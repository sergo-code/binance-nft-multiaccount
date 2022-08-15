# binance-nft-multiaccount

- Automating the process of sending a program to the server and launching it  
- Made to quickly launch multiple accounts  
- binanceNFT is a stub that demonstrates the operation of the program: authorization and sending user data to you in a telegram
### tmux 
[tmux](https://github.com/tmux/tmux/wiki/Getting-Started) is installed on the servers so as not to lose the session when disconnecting.

Connections to an active session on the server:  
```
tmux a -t test
```
Exiting the session: 
- Leave to work in the background: CTRL+B  D  
- Stop working: CTRL+D  

### Launch
1) Fill in the file profiles.xlsx
2) Fill in the telegram data in the file binanceNFT/config_template.py
3) Install all dependencies 
```
pip install -r requirements.txt
```
4) Start the program  
```
python3 main.py
```
### Сustomization
- For Binance:  
  - Add your program to the binanceNFT directory and replace the config so that authorization data is transmitted.  
- Not for Binance:  
  - Replace the binanceNFT directory with your own  
  - In main.py define excel table headers  
  - Edit config.py  
  - In functions.py change the logic of the application launch
