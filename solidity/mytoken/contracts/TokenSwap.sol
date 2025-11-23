// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/**
 * @title TokenSwap
 * @dev A simple DEX contract for swapping tokens
 * This contract maintains liquidity pools for token pairs
 */
contract TokenSwap {
    // Mapping from token address to its reserve
    mapping(address => uint256) public reserves;
    
    // Exchange rate: 1 tokenA = rate tokenB (scaled by 1e18)
    mapping(address => mapping(address => uint256)) public exchangeRates;
    
    // Liquidity provider addresses
    address[] public liquidityProviders;
    mapping(address => bool) public isLiquidityProvider;
    
    // Owner of the contract
    address public owner;
    
    // Fee percentage (in basis points, e.g., 30 = 0.3%)
    uint256 public constant FEE_BPS = 30;
    
    event Swap(
        address indexed tokenIn,
        address indexed tokenOut,
        address indexed user,
        uint256 amountIn,
        uint256 amountOut
    );
    
    event LiquidityAdded(
        address indexed token,
        address indexed provider,
        uint256 amount
    );
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @dev Add liquidity to a token pool
     */
    function addLiquidity(address token, uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        reserves[token] += amount;
        
        if (!isLiquidityProvider[msg.sender]) {
            liquidityProviders.push(msg.sender);
            isLiquidityProvider[msg.sender] = true;
        }
        
        emit LiquidityAdded(token, msg.sender, amount);
    }
    
    /**
     * @dev Set exchange rate between two tokens
     * @param tokenA First token address
     * @param tokenB Second token address
     * @param rate Exchange rate (1 tokenA = rate tokenB, scaled by 1e18)
     */
    function setExchangeRate(address tokenA, address tokenB, uint256 rate) external onlyOwner {
        require(rate > 0, "Rate must be greater than 0");
        exchangeRates[tokenA][tokenB] = rate;
        // Set inverse rate
        exchangeRates[tokenB][tokenA] = (1e18 * 1e18) / rate;
    }
    
    /**
     * @dev Swap tokens
     * @param tokenIn Address of token to swap from
     * @param tokenOut Address of token to swap to
     * @param amountIn Amount of tokenIn to swap
     * @return amountOut Amount of tokenOut received
     */
    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external returns (uint256 amountOut) {
        require(amountIn > 0, "Amount must be greater than 0");
        require(reserves[tokenIn] >= amountIn, "Insufficient liquidity");
        require(exchangeRates[tokenIn][tokenOut] > 0, "Exchange rate not set");
        
        // Transfer tokens from user
        IERC20(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        
        // Calculate output amount using exchange rate
        uint256 rate = exchangeRates[tokenIn][tokenOut];
        amountOut = (amountIn * rate) / 1e18;
        
        // Apply fee (deduct fee from output)
        uint256 fee = (amountOut * FEE_BPS) / 10000;
        amountOut -= fee;
        
        // Check if we have enough reserves
        require(reserves[tokenOut] >= amountOut, "Insufficient reserves");
        
        // Update reserves
        reserves[tokenIn] += amountIn;
        reserves[tokenOut] -= amountOut;
        
        // Transfer tokens to user
        IERC20(tokenOut).transfer(msg.sender, amountOut);
        
        emit Swap(tokenIn, tokenOut, msg.sender, amountIn, amountOut);
        
        return amountOut;
    }
    
    /**
     * @dev Get quote for swap without executing
     */
    function getQuote(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external view returns (uint256 amountOut) {
        require(exchangeRates[tokenIn][tokenOut] > 0, "Exchange rate not set");
        uint256 rate = exchangeRates[tokenIn][tokenOut];
        amountOut = (amountIn * rate) / 1e18;
        uint256 fee = (amountOut * FEE_BPS) / 10000;
        amountOut -= fee;
        return amountOut;
    }
    
    /**
     * @dev Get reserve for a token
     */
    function getReserve(address token) external view returns (uint256) {
        return reserves[token];
    }
}

