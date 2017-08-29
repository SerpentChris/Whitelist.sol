pragma solidity ^0.4.0;

contract Whitelist {
    address public owner;
    mapping(address => bool) permitted;

    modifier restricted{
        assert(msg.sender == owner);
        _;
    }
    function Whitelist(){
        owner = msg.sender;
    }
    function add(address addr) restricted{
        permitted[addr] = true;
    }
    function add_all(address[] addrs) restricted{
        uint l = addrs.length;
        for(uint i = 0; i < l; i++){
            permitted[addrs[i]] = true;
        }
    }
    function remove(address addr) restricted{
        permitted[addr] = false;
    }
    function check(address addr) returns (bool){
        return permitted[addr];
    }
    function destroy() restricted{
        selfdestruct(owner);
    }
}
