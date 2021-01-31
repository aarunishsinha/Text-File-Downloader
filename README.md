# Text-File-Downloader
COL334 - Computer Networks

A large text file of about 6.5MB is available at http://vayu.iitd.ac.in/big.txt and \
http://norvig.com/big.txt. Some details are given below: \
MD5 sum: 70a4b9f4707d258f559f91615297a3ec\
Size: 6488666 bytes

The tool is supposed to download this file quickly, and also be resilient to disconnections, Eg. if your network is poor and disconnects while a file transfer is in progress then we want that the tool should resume downloading the file from the point of last disconnection and not download the same portions twice.

The final program, which is resilient to disconnections, and takes as input a CSV file with the following structure:

[URL-1 for the object], [Number of parallel TCP connections to this URL] 

[URL-2 for the object], [Number of parallel TCP connections to this URL] 

...

In this project, I have used thread to experiment with:
- Number of parallel TCP connections open to the server.
- Variation with the download speed on increasing the number of TCP connections. 

![alt text](https://github.com/aarunishsinha/Text-File-Downloader/blob/main/plot1.png)
- Time taken by each TCP connection.

![alt text](https://github.com/aarunishsinha/Text-File-Downloader/blob/main/Figure_1.png)
- Change in download speed on spreading the connections between different servers.

In case a TCP connection breaks, the thread does not end but tries to open a new connection. Whenever a new connection succeeds, the thread resumes to download more chunks. 
