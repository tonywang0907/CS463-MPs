import java.math.BigInteger;
import java.util.Random;
/**
 * Created by naveed on 2/15/15.
 */
public class Server {
    public static void main(String[] args) 
    {
        Boolean debug=false;
    	if(args.length != 2) { System.out.println("Invalid arguments, exiting..."); return; }
    	
        String filename = args[0];
        String clientFilename = args[1];
	
        Inputs inputs = new Inputs(filename);

        BigInteger[] serverInputs = inputs.getInputs();

        BigInteger[] encryptedPolyCoeffs = (BigInteger[])StaticUtils.read(clientFilename);
        BigInteger publicKey = (BigInteger)StaticUtils. read("ClientPK.out");

        Paillier paillier = new Paillier();
        paillier.setPublicKey(publicKey);

        BigInteger[] encryptedPolyEval = new BigInteger[serverInputs.length];

        /* TODO: implement server-side protocol here.
         * For each sj in serverInputs:
			- Pick a random rj
			- Homomorphically evaluate P(sj)
			- Compute E_K(rj P(sj) + sj)
			- Set encryptedPolyEval[j] = E_K(rj P(sj) + sj)
        */
 	    // ------ Your code goes here. --------
        
        // m = serverInputs.length
        for (int j = 0; j < serverInputs.length; j++) {

            // Evaluate PSJ
            BigInteger encryptedPSJ = BigInteger.ZERO;

            BigInteger sJ = serverInputs[j];

            // n = encryptedPolyCoeffs.length
            for (int l = 0; l < encryptedPolyCoeffs.length; l++) {
                
                // Compute using multiplication by a constant
                BigInteger sJL = sJ.pow(l);

                encryptedPSJ = paillier.add(encryptedPSJ, paillier.const_mul(encryptedPolyCoeffs[l], sJL));
            }

            // Computer RJ
            BigInteger rJ = randomBigInt(sJ);

            // Compute E_K(rj P(sj) + sj)
            BigInteger encryptedKey = paillier.add(paillier.const_mul(rJ, encryptedPSJ), paillier.Encryption(sJ));

            // Set encryptedPolyEval[j] = E_K(rj P(sj) + sj)
            encryptedPolyEval[j] = encryptedKey;

        }

        StaticUtils.write(encryptedPolyEval, clientFilename+".out");
    }

    //This is not cryptographically secure random number.
    public static BigInteger randomBigInt(BigInteger n) 
    {
        Random rand = new Random();
        BigInteger result = new BigInteger(n.bitLength(), rand);
        while( result.compareTo(n) >= 0 ) {
            result = new BigInteger(n.bitLength(), rand);
        }
        return result;
    }
}
