Setup
=====

### 1. Package Installation (Client & Server) ###

pacman -S wireguard-tools

### 2. Nftables Configuration (Server) ###

/etc/nftables.conf:
```
table inet filter {
  chain input {
    ...
    udp dport 1234 accept comment "wireguard"
    ...
  }

  chain forward {
    type filter hook forward priority 0; policy drop;

    ct state invalid counter drop
    iifname wg0 oifname ens3 accept
    iifname ens3 oifname wg0 ct state related,established accept

    log counter drop
  }
}

table inet router {
  chain prerouting {
    type nat hook prerouting priority -100;
  }

  chain postrouting {
    type nat hook postrouting priority 100;

    ip saddr 10.10.10.0/24 oifname ens3 masquerade
    ip6 saddr fc10:10:10::0/64 oifname ens3 masquerade
  }
}
```

### 3. Sysctl Configuration (Server) ###

/etc/sysctl.d/99-wireguard.conf:
```
net.ipv4.ip_forward=1
net.ipv6.conf.all.forwarding=1
```

### 4. Keys Generation (Server) ###

public & private keys:
```
cd /etc/wireguard/
(umask 0077; wg genkey | tee server.key | wg pubkey > server.key.pub)
```

### 5. Keys Generation (Client) ###

public & private keys:
```
cd /etc/wireguard/
(umask 0077; wg genkey | tee client.key | wg pubkey > client.key.pub)
```

pre-shared key:
```
wg genpsk
```

### 6. Wireguard (Server) ###

/etc/wireguard/wg0.conf:
```
# server
[Interface]
PrivateKey = ...
ListenPort = 1234
Address = 10.10.10.1/24, fc10:10:10::1/64
MTU = 1280

# client
[Peer]
PublicKey = ...
PresharedKey = ...
AllowedIPs = 10.10.10.2/32, fc10:10:10::2/128
PersistentKeepalive = 25

# another client
#[Peer]
#PublicKey = ...
#PresharedKey = ...
#AllowedIPs = 10.10.10.3/32, fc10:10:10::3/128
#PersistentKeepalive = 25
```

### 7. Wireguard (Client) ###

/etc/wireguard/wg0.conf:
```
# client
[Interface]
PrivateKey = ...
Address = 10.10.10.2/24, fc10:10:10::2/64
#DNS = 1.1.1.1, 1.0.0.1, 8.8.8.8, 8.8.4.4, 2606:4700:4700::1111, 2606:4700:4700::1001, 2001:4860:4860::8888, 2001:4860:4860::8844
MTU = 1280

# server
[Peer]
PublicKey = ...
PresharedKey = ...
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = vale.re:1234
```

### 8. QR Code (Client) ###

For mobile phone settings via the Wireguard app:
```
qrencode -t ansiutf8 < client.conf
```

### 9. Enable and start systemd service (Client & Server)

```
systemctl enable wg-quick@wg0.service
systemctl start wg-quick@wg0.service
```

Documentation
=============

Some (more or less) interesting links:  

https://wiki.archlinux.org/title/WireGuard  
https://emanuelduss.ch/2018/09/29/wireguard-vpn-road-warrior-setup/  
https://github.com/pirate/wireguard-docs  
https://jwcxz.com/notes/200702-simple-wireguard-vpn/  
https://xdeb.org/post/2019/09/26/setting-up-a-server-firewall-with-nftables-that-support-wireguard-vpn/  
https://gist.github.com/Gunni/5deaf9b8b65b212cbfcf9aab6fa46820  
https://github.com/Fruxlabs/wireguard-roadwarrior/blob/master/wireguard-install.sh  
https://blog.levine.sh/14058/wireguard-on-k8s-road-warrior-style-vpn-server  
https://www.ivpn.net/knowledgebase/linux/linux-wireguard-kill-switch/  
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/securing_networks/getting-started-with-nftables_securing-networks  
