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
    return false;
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
