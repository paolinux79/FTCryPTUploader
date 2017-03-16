# FTCryPTUploader
A multithreaded encrypting ftp uploader.

------------
FTCryPTUploader is a small python3 script written to upload files to an FTP server while crypting them. It is focused on

 - avoiding any unnecessary disk accesses
 - keeping a very low memory footprint

It uses AES Cipher in EBC mode to encrypt and PKCS#7 to pad.
The only "extra" requirements is pyCrypto.



Released under the BSD 2-Clause License