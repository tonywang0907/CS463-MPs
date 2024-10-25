package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.IOException;

public class Checkpoint1 {
	private Block block;

	public Checkpoint1() {
		String blockHash = "000000000000000f5795bfe1de0381a44d4d5ea2ad81c21d77f275bffa03e8b3";
		BlockExplorer explorer = new BlockExplorer();
		try {
			block = explorer.getBlock(blockHash);
		} catch (APIException | IOException e) {
			e.printStackTrace();
			block = null;
		}
	}

	public Checkpoint1(String blockHash) {
		BlockExplorer explorer = new BlockExplorer();
		try {
			block = explorer.getBlock(blockHash);
		} catch (APIException | IOException e) {
			e.printStackTrace();
			block = null;
		}
	}
	/**
	 * Blocks-Q1: What is the size of this block?
	 *
	 * Hint: Use method getSize() in Block.java
	 *
	 * @return size of the block
	 */
	public long getBlockSize() {
		// TODO implement me
		if (block != null) {
			return block.getSize();
		} else {
			System.out.println("block detected to be null.");
			return -1;
		}
	}

	/**
	 * Blocks-Q2: What is the Hash of the previous block?
	 *
	 * Hint: Use method getPreviousBlockHash() in Block.java
	 *
	 * @return hash of the previous block
	 */
	public String getPrevHash() {
		// TODO implement me
		if (block != null) {
			return block.getPreviousBlockHash();
		} else {
			System.out.println("block detected to be null.");
			return "";
		}
	}

	/**
	 * Blocks-Q3: How many transactions are included in this block?
	 *
	 * Hint: To get a list of transactions in a block, use method
	 * getTransactions() in Block.java
	 *
	 * @return number of transactions in current block
	 */
	public int getTxCount() {
		// TODO implement me
		if (block != null) {
			return block.getTransactions().size();
		} else {
			System.out.println("block detected to be null.");
			return 0;
		}
	}

	/**
	 * Transactions-Q1: Find the transaction with the most outputs, and list the
	 * Bitcoin addresses of all the outputs.
	 *
	 * Hint: To get the bitcoin address of an Output object, use method
	 * getAddress() in Output.java
	 *
	 * @return list of output addresses
	 */
	public List<String> getOutputAddresses() {
		// TODO implement me
		List<String> outputAddresses = new ArrayList<>();
		Transaction transactionMax = null;

		if (block != null) {
			for (Transaction transaction : block.getTransactions()) {
				if (transactionMax == null || transaction.getOutputs().size() > transactionMax.getOutputs().size()) {
					transactionMax = transaction;
				}
			}

			for (Output transactionOutput : transactionMax.getOutputs()) {
				outputAddresses.add(transactionOutput.getAddress());
			}
			return outputAddresses;
		} else {
			System.out.println("block detected to be null.");
			return outputAddresses;
		}

	}

	/**
	 * Transactions-Q2: Find the transaction with the most inputs, and list the
	 * Bitcoin addresses of the previous outputs linked with these inputs.
	 *
	 * Hint: To get the previous output of an Input object, use method
	 * getPreviousOutput() in Input.java
	 *
	 * @return list of input addresses
	 */
	public List<String> getInputAddresses() {
		// TODO implement me
		List<String> inputAddresses = new ArrayList<>();
		Transaction transactionMax = null;

		if (block != null) {
			for (Transaction transaction : block.getTransactions()) {
				if (transactionMax == null || transaction.getInputs().size() > transactionMax.getInputs().size()) {
					transactionMax = transaction;
				}
			}

			for (Input tranactionInput : transactionMax.getInputs()) {
				inputAddresses.add(tranactionInput.getPreviousOutput().getAddress());
			}

			return inputAddresses;
		} else {
			System.out.println("block detected to be null.");
			return inputAddresses;
		}
	}

	/**
	 * Transactions-Q3: What is the bitcoin address that has received the
	 * largest amount of Satoshi in a single transaction?
	 *
	 * Hint: To get the number of Satoshi received by an Output object, use
	 * method getValue() in Output.java
	 *
	 * @return the bitcoin address that has received the largest amount of Satoshi
	 */
	public String getLargestRcv() {
		// TODO implement me
		String largestReceiverAddress = null;
		long largestAmount = 0;

		if (block != null) {
			for (Transaction transaction : block.getTransactions()) {
				for (Output output : transaction.getOutputs()) {
					if (output.getValue() > largestAmount) {
						largestReceiverAddress = output.getAddress();
						largestAmount = output.getValue();
					}
				}

			}
			return largestReceiverAddress;
		} else {
			System.out.println("block detected to be null.");
			return "";
		}

	}

	/**
	 * Transactions-Q4: How many coinbase transactions are there in this block?
	 *
	 * Hint: In a coinbase transaction, getPreviousOutput() == null --> although this matches with the documentation, the result is wrong.
	 * Even if it's a coinbase transactions, it's not null during my test.
	 * I would recommend another work around that a coinbase transaction should have the sum of getPreviousOutput().getValue() equal to 0 because the total input should be 0.
	 * You can see an example of coinbase transaction here: https://www.blockchain.com/btc/tx/cdab676fe718b5155251f15b275c5f92ad965ee8557270d1eec07ccc42d4aaaf
	 * I'm using Java 1.8.0_242, if anyone made it success with getPreviousOutput() == null, please email me or send a campuswire post. Much appreciated!
	 *
	 * @return number of coin base transactions
	 */
	public int getCoinbaseCount() {
		// TODO implement me
		int coinbaseCount = 0;

		if (block != null) {
			for (Transaction transaction : block.getTransactions()) {
				for (Input input : transaction.getInputs()) {
					if (input.getPreviousOutput().getValue() == 0) {
						coinbaseCount += 1;
						break;
					}
				}
			}
			return coinbaseCount;
		} else {
			System.out.println("block detected to be null.");
			return coinbaseCount;
		}
	}

	/**
	 * Transactions-Q5: What is the number of Satoshi generated in this block?
	 *
	 * @return number of Satoshi generated
	 */
	public long getSatoshiGen() {
		// TODO implement me
		long totalSatoshiGenerated = 0;

		if (block != null) {
			for (Transaction transaction : block.getTransactions()) {
				boolean isCoinbaseTransaction = false;

				for (Input input : transaction.getInputs()) {
					if (input.getPreviousOutput().getValue() == 0) {
						isCoinbaseTransaction = true;
					}
				}

				if (isCoinbaseTransaction) {
					for (Output output : transaction.getOutputs()) {
						totalSatoshiGenerated += output.getValue();
					}
				}
			}
			return totalSatoshiGenerated;
		} else {
			System.out.println("block detected to be null.");
			return -1;	
		}
	}
}
