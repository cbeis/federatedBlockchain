// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.3;
import "node_modules/@openzeppelin/contracts/access/Ownable.sol";

interface PrototypeInterface {
  function callback(string memory _data) external;
}

contract DataOracle is Ownable{

  event GetLatestDataEvent(address callerAddress);
  event SetLatestDataEvent(string data, address callerAddress);


  function getLatestData() public{
    emit GetLatestDataEvent(msg.sender);
    validation = "True";
    return;
  }

  function setLatestData(string memory _data, address _callerAddress) public onlyOwner {
    PrototypeInterface prototypeInstance;
    prototypeInstance = PrototypeInterface(_callerAddress);
    prototypeInstance.callback(_data);
    validation = "False";
    emit SetLatestDataEvent(_data, _callerAddress);
  }
}