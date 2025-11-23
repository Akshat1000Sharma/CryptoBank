// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/**
 * @title MyToken2
 * @dev A second ERC20 token for swap functionality
 */
contract MyToken2 is ERC20 {
    constructor(uint256 initialSupply) ERC20("MyToken2", "MTK2") { 
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }
}

