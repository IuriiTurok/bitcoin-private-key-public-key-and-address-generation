import bitcoin
import qrcode
import urllib3

count=0
while True:
  #generate a random private key
  valid_private_key = False
  while not valid_private_key:
    private_key = bitcoin.random_key()
    decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
    valid_private_key = 0 < decoded_private_key < bitcoin.N 

  print ('Private Key (hex) is: ' + private_key)
  print ('private Key (decimal) is: ' + str(decoded_private_key))

  #convert private key to WIF format
  wif_encoded_private_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
  print('Private Key (WIF) is: ' + wif_encoded_private_key)

  # Add sufix '01' to indicate a compressed private Key
  compressed_private_key = private_key + '01'
  print ('Private Key Compressed (hex) is: ' + compressed_private_key)

  # generate a WIF format from the compressed private key (WIF-compressed)
  wif_compressed_private_key = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_private_key, 'hex'), 'wif')
  print ('Private Key (WIF-compressed) is: ' + wif_compressed_private_key) 

  # Multiply de EC generator G with the priveate key to get a public key point
  public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
  print ('Public Key (x,y) coordinates are: ' + str(public_key))

  # Encode as hex, prefix 04
  hex_encoded_public_key = bitcoin.encode_pubkey(public_key, 'hex')
  print ('Public Key (hex) is: ' + hex_encoded_public_key)

  # Compress public key, adjust prefix depending on whether y is even or odd
  (public_key_x, public_key_y) = public_key
  if public_key_y % 2 == 0:
    compressed_prefix = '02'
  else:
    compressed_prefix = '03'
  hex_compressed_public_key = compressed_prefix + bitcoin.encode(public_key_x, 16)
  print ('Compressed Public Key is: ' + hex_compressed_public_key)

  # Generate bitcoin address from public Key
  print ('Bitcoin Address (b58check) is: ' + bitcoin.pubkey_to_address(public_key))

  # Generate compressedd bitcoin address from compressed public key 
  print ('Compressed Bitcoin Address (b58check) is: ' + bitcoin.pubkey_to_address(hex_compressed_public_key))

  compressed_address_base58check = bitcoin.pubkey_to_address(hex_compressed_public_key)

  # Qrcode generator from compressed_address_base58check
  # img = qrcode.make(compressed_address_base58check)

  satoshiadress = '1EzwoHtiXB4iFwedPr49iywjZn2nnekhoj'
  http = urllib3.PoolManager()
  r = http.request('GET', 'https://blockchain.info/q/addressbalance/'+  compressed_address_base58check +'?confirmations=1')

  if r.data == b'0' :
    print ('0')    
  else: 
    print ('+')
  print (r.data)
  count += 1
  if count >= 5: break

#satoshiadress = '1EzwoHtiXB4iFwedPr49iywjZn2nnekhoj'
#api_request = 'https://blockchain.info/q/addressbalance/'+  keyToAddr(private_key) +'?confirmations=1'

#api_request = 'https://blockchain.info/q/addressbalance/'+  hex_compressed_public_key +'?confirmations=1'
#request1 = urllib.request(api_request)
#response_body = urllib.urlopen(request1).read()
#print ('Balance: ', response_body)
