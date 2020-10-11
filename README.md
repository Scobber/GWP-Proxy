# GWP-Proxy
LoraWan GWP proxy

To use, 

python3 proxy.py

```
--raddress sets upstream router address
--rport sets upstream router port
--listen sets listener IP. 0.0.0.0 binds all
--port sets listener port
```

Change your gateways to use the proxy, and the bi-directional comms will be available on stdout

Use case : [https://thescobber.com/2020/10/07/proxying-gwp-packets/](https://thescobber.com/2020/10/07/proxying-gwp-packets/).
