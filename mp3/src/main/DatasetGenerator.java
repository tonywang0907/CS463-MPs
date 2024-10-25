package main;
import info.blockchain.api.blockexplorer.*;
import info.blockchain.api.blockexplorer.entity.*;
import info.blockchain.api.*;
import java.lang.*;

import java.util.*;
import java.io.FileWriter;
import java.io.IOException;


public class DatasetGenerator {
	String file;

	public DatasetGenerator(String file) {
		this.file = file;
	}

	public boolean writeTransactions() {
		// TODO implement me
		BlockExplorer explorer = new BlockExplorer();

		try (FileWriter writer = new FileWriter(file)) {
			int startHeight = 265852;
			int endHeight = 266085;

			for (int height = startHeight; height <= endHeight; height++) {
				List<Block> blocks = explorer.getBlocksAtHeight(height);

				for (Block block : blocks) {
					List<Transaction> transactions = block.getTransactions();
					
					for (Transaction transaction : transactions) {
						// Check if it's a coinbase transaction
						boolean isCoinbaseTransaction = false;
						for (Input input : transaction.getInputs()) {
							if (input.getPreviousOutput().getValue() == 0) {
								isCoinbaseTransaction = true;
								break;
							}
						}

						// Skip coinbase transaction 
						if (isCoinbaseTransaction) {
							continue;
						}

						String transactionHash = transaction.getHash();

						// Record all inputs
						for (Input input : transaction.getInputs()) {
							String inputRecord = generateInputRecord(transactionHash, input.getPreviousOutput().getAddress(), input.getPreviousOutput().getValue());
							writer.write(inputRecord + "\n");
						}

						// Record all outputs 
						for (Output output : transaction.getOutputs()) {
							String outputRecord = generateOutputRecord(transactionHash, output.getAddress(), output.getValue());
							writer.write(outputRecord + "\n");
						}
					}
				}
			}
			writer.close();
			return true;
		} catch (APIException | IOException e) {
			e.printStackTrace();
			return false;
		}
	}

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Previous output address of the input
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the input
	 */
	private String generateInputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " in";
	}

	/**
	 * Generate a record in the transaction dataset
	 *
	 * @param txHash
	 *            Transaction hash
	 * @param address
	 *            Output bitcoin address
	 * @param value
	 *            Number of Satoshi transferred
	 * @return A record of the output
	 */
	private String generateOutputRecord(String txHash,
			String address, long value) {
		return txHash + " " + address + " " + value + " out";
	}
}
