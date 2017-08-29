from ethereum.tools import tester
import subprocess
import os
import json
import binascii


def sol_compile(code_path, optimized: bool=False):
    code_path = os.path.abspath(code_path)
    code_name = os.path.basename(code_path)

    solc_args = ['solc', '--bin']
    if optimized:
        solc_args.append('--optimize')
    solc_args.append(code_path)

    solc_output = subprocess.check_output(solc_args)
    solc_output = solc_output.decode().split('\n')
    for i, line in enumerate(solc_output):
        if code_name in line:
            break
    code_evm = binascii.unhexlify(''.join(solc_output[i + 2:]).strip())

    solc_output = subprocess.check_output(['solc', '--abi', code_path])
    solc_output = solc_output.decode().split('\n')
    for i, line in enumerate(solc_output):
        if code_name in line:
            break
    code_abi = json.loads(''.join(solc_output[i + 2:]).strip())

    return code_evm, code_abi


def main():
    c = tester.Chain()
    owner = tester.a0
    owner_key = tester.k0

    whitelist_evm, whitelist_abi = sol_compile('whitelist.sol')
    addr = c.contract(whitelist_evm, language='evm', sender=owner_key)
    whitelist = tester.ABIContract(c, whitelist_abi, addr)

    assert binascii.unhexlify(whitelist.owner()[2:]) == owner

    whitelist.add(owner)
    assert whitelist.check(owner)
    addresses = [tester.a1, tester.a2, tester.a3]
    whitelist.add_all(addresses)
    assert all(map(whitelist.check, addresses))
    whitelist.remove(owner)
    assert not whitelist.check(owner)
    for a in addresses:
        whitelist.remove(a)
        assert not whitelist.check(a)
    whitelist.destroy()

    print('TEST PASSED')

if __name__ == '__main__':
    main()