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
    string public prototypeAccuracy;
    string public prototype;

    DataOracleInterface private oracleInstance;

    mapping (address => bool) private Owners;

    event newOracleAddressEvent(address oracleAddress);

    function _addPrototype(string memory _prototype, string memory _prototypeAccuracy ) public allowedOwner{
        prototype = _prototype;
        prototypeAccuracy = _prototypeAccuracy;
        delete oracleData;
    }

    function _seeAll() public view allowedOwner returns (string memory, string memory, string memory){
        return (prototypeAccuracy,prototype,oracleData);
    }

    function _checkAccuracy(string memory _prototypeAccuracy) public view allowedOwner returns (bool){
        return (keccak256(abi.encodePacked(prototypeAccuracy))== keccak256(abi.encodePacked(_prototypeAccuracy)));
    }

    function setOwner(address _owner) public onlyOwner {
        Owners[_owner]=true;
    }

    function contains() private view returns (bool){
        return Owners[msg.sender];
    }

    function setOracleInstanceAddress (address _oracleInstanceAddress) public onlyOwner {
        oracleAddress = _oracleInstanceAddress;
        oracleInstance = DataOracleInterface(oracleAddress);
        emit newOracleAddressEvent(oracleAddress);
    }

    function updateData() public {
        oracleInstance.getLatestData();
    }

    function callback(string memory _oracleData) public onlyOracle {
      oracleData = string(abi.encodePacked(oracleData,' ',_oracleData));
    }

    modifier allowedOwner() {
        require(contains(), "You are not authorized to call this function.");
        _;
    }

    modifier onlyOracle() {
      require(msg.sender == oracleAddress, "You are not authorized to call this function.");
      _;
    }
}