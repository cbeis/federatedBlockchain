// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.3;
import "node_modules/@openzeppelin/contracts/access/Ownable.sol";

interface DataOracleInterface {
  function getLatestData() external;
}

contract PrototypeBuffer is Ownable{

    address[] public owners;
    string private oracleData;
    address private oracleAddress;

    DataOracleInterface private oracleInstance;

    mapping (address => string) public ownerToPrototype;
    mapping (address => bool) private Owners;

    event newOracleAddressEvent(address oracleAddress);
    event ReceivedNewRequestIdEvent(string id);
    event DataUpdatedEvent(string oracleData);

    function _addPrototype(string memory _prototype ) public {
        ownerToPrototype[msg.sender] = _prototype;
        if(!contains()){
        owners.push(msg.sender);
        setOwner();
        }
    }

    function _getPrototype() public view returns (string memory){
        return ownerToPrototype[msg.sender];
    }

    function _seeAll() public returns (string[] memory){
        string[] memory prototypes = new string[](2*owners.length +1);
        for (uint i = 0; i < owners.length; i++) {
            address _owner = owners[i];
            prototypes[2*i] = toAsciiString(_owner);
            prototypes[(2*i) + 1] = ownerToPrototype[_owner] ;
        }
        prototypes[prototypes.length -1] = oracleData;
        //In oracle, we can't delete data, the keyword "delete" is just assign a default value to a determined variable.
        delete oracleData;
        return prototypes;
    }

    function contains() private view returns (bool){
        return Owners[msg.sender];
    }

    function setOwner() private {
        Owners[msg.sender]=true;
    }

    function toAsciiString(address x) public pure returns (string memory) {
        bytes memory s = new bytes(40);
        for (uint i = 0; i < 20; i++) {
            bytes1 b = bytes1(uint8(uint(uint160(x)) / (2**(8*(19 - i)))));
            bytes1 hi = bytes1(uint8(b) / 16);
            bytes1 lo = bytes1(uint8(b) - 16 * uint8(hi));
            s[2*i] = char(hi);
            s[2*i+1] = char(lo);
        }
    return string(abi.encodePacked("0x",s));
    }
    function char(bytes1 b) public pure returns (bytes1 c) {
        if (uint8(b) < 10) return bytes1(uint8(b) + 0x30);
        else return bytes1(uint8(b) + 0x57);
    }

    function setOracleInstanceAddress (address _oracleInstanceAddress) public onlyOwner {
        oracleAddress = _oracleInstanceAddress;
        oracleInstance = DataOracleInterface(oracleAddress);
        emit newOracleAddressEvent(oracleAddress);
    }

    function updateData() public {
        oracleInstance.getLatestData();
        emit ReceivedNewRequestIdEvent("Query to oracle.");
    }

    function callback(string memory _oracleData) public onlyOracle {
      oracleData = _oracleData;
      emit DataUpdatedEvent(oracleData);
    }

    modifier onlyOracle() {
      require(msg.sender == oracleAddress, "You are not authorized to call this function.");
      _;
    }
}