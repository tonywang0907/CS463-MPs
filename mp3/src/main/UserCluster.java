package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.Math;

public class UserCluster {
	private Map<Long, List<String>> userMap; // Map a user id to a list of
												// bitcoin addresses
	private Map<String, Long> keyMap; // Map a bitcoin address to a user id

	private HashMap<String, List<String>> cluster;
	
	private long userIdCounter; 

	int hash_index = 0;
	int addr_index = 1;
	int val_index  = 2;
	int type_index = 3;
	int column_len = 4;

	public UserCluster() {
		userMap = new HashMap<Long, List<String>>();
		keyMap = new HashMap<String, Long>();
		cluster = new HashMap<String, List<String>>();
		userIdCounter = 0;
	}

	/**
	 * Read transactions from file
	 *
	 * @param file
	 * @return true if read succeeds; false otherwise
	 */
	public boolean readTransactions(String file) {
		// TODO implement me
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;

            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(" ");
                if (parts.length < column_len) {
                    System.out.println("Invalid format: " + line);
                    continue;   
                }

                String transactionHash = parts[hash_index];
                String bitcoinAddress = parts[addr_index];
                String recordType = parts[type_index];

				if (recordType.equals("in")) {
					cluster.putIfAbsent(transactionHash, new ArrayList<>());
					cluster.get(transactionHash).add(bitcoinAddress);  
				} 

				if (recordType.equals("out")) {
					if (!keyMap.containsKey(bitcoinAddress))  {
						userIdCounter++;
						keyMap.put(bitcoinAddress, userIdCounter);
						userMap.putIfAbsent(userIdCounter, new ArrayList<>());
						userMap.get(userIdCounter).add(bitcoinAddress);
					}
				}
            }
            return true; 
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
	}

	public void mergeAddresses() {
		for (List<String> addresses : cluster.values()) {
			long mergeUserId = -1L;  

			// Find smallest existing userId (for merging)
			for (String address : addresses) {
				if (keyMap.containsKey(address)) {
					long userId = keyMap.get(address);
					if (mergeUserId == -1L || userId < mergeUserId) {
						mergeUserId = userId;  
					}
				}
			}

			if (mergeUserId == -1L) {
				mergeUserId = ++userIdCounter;
				userMap.putIfAbsent(mergeUserId, new ArrayList<>());
			}

			// Merging
			for (String address : addresses) {
				if (keyMap.containsKey(address)) {
					long userId = keyMap.get(address);
					if (userId != mergeUserId) {
						List<String> mergeAddresses = userMap.get(userId);
						if (mergeAddresses != null) {
							for (String addr : mergeAddresses) {
								keyMap.put(addr, mergeUserId); // Update keyMap
								if (!userMap.get(mergeUserId).contains(addr)) {
									userMap.get(mergeUserId).add(addr);  // Add to new cluster
								}
							}
						}
						userMap.remove(userId); // after merge parsing
					}
				}
				keyMap.put(address, mergeUserId);
				if (!userMap.get(mergeUserId).contains(address)) {
					userMap.get(mergeUserId).add(address);
				}
			}
		}
	}

	/**
	 * Return number of users (i.e., clusters) in the transaction dataset
	 *
	 * @return number of users (i.e., clusters)
	 */
	public int getUserNumber() {
		// TODO implement me
		return userMap.size();
	}

	/**
	 * Return the largest cluster size
	 *
	 * @return size of the largest cluster
	 */
	public int getLargestClusterSize() {
		// TODO implement me
		int largestClusterSize = 0;

		for (List<String> clusterAddresses : userMap.values()) {
			if (clusterAddresses.size() > largestClusterSize) {
				largestClusterSize = clusterAddresses.size();
			}
		}
		
		return largestClusterSize;
	}

	public boolean writeUserMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (long user : userMap.keySet()) {
				List<String> keys = userMap.get(user);
				w.write(user + " ");
				for (String k : keys) {
					w.write(k + " ");
				}
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing user list!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeKeyMap(String file) {
		try {
			BufferedWriter w = new BufferedWriter(new FileWriter(file));
			for (String key : keyMap.keySet()) {
				w.write(key + " " + keyMap.get(key) + "\n");
				w.newLine();
			}
			w.flush();
			w.close();
		} catch (IOException e) {
			System.err.println("Error in writing key map!");
			e.printStackTrace();
			return false;
		}

		return true;
	}

	public boolean writeUserGraph(String txFile, String userGraphFile) {
	     try {
                        BufferedReader r1 = new BufferedReader(new FileReader(txFile));
                        Map<String, Long> txUserMap = new HashMap<String, Long>();
                        String nextLine;
                        while ((nextLine = r1.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r1.close();
                                        return false;
                                }
                                if (s[type_index].equals("in") && !txUserMap.containsKey(s[hash_index])) { // new transaction
                                        Long user;
                                        if ((user=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                System.out.println(nextLine);
                                                r1.close();
                                                return false;
                                        }
                                        txUserMap.put(s[hash_index], user);
                                }
                        }
                        r1.close();

                        BufferedReader r2 = new BufferedReader(new FileReader(txFile));
                        BufferedWriter w = new BufferedWriter(new FileWriter(userGraphFile));
                        while ((nextLine = r2.readLine()) != null) {
                                String[] s = nextLine.split(" ");
                                if (s.length < column_len) {
                                        System.err.println("Invalid format: " + nextLine);
                                        r2.close();
                                        w.flush();
                                        w.close();
                                        return false;
                                }
                                if (s[type_index].equals("out")) {
                                        if(txUserMap.get(s[hash_index]) == null) {
                                                System.err.println("Did not find input transaction for Tx: " + s[hash_index]);
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        long inputUser = txUserMap.get(s[hash_index]);
                                        Long outputUser;
                                        if ((outputUser=keyMap.get(s[addr_index])) == null) {
                                                System.err.println(s[addr_index] + " is not in the key map!");
                                                r2.close();
                                                w.flush();
                                                w.close();
                                                return false;
                                        }
                                        w.write(inputUser + "," + outputUser + "," + s[val_index] + "\n");
                                }
                        }
                        r2.close();
                        w.flush();
                        w.close();
                } catch (IOException e) {
                        e.printStackTrace();
                }
                return true;

	}

}
