# Setup the BHP LIMS Virtual machine

First, install Ubuntu Server Xenial 16.04 LTS in the VM
https://www.ubuntu.com/download/alternative-downloads

After the base system installation, and in order to be able to use ansible
playbook to setup the instance, we need to setup the Virtual Machine properly:

## Add senaite user to sudoers

```sh
sudo nano /etc/sudoers.d/senaite
```

Add the following:

```sh
# User rules for SENAITE
senaite ALL=(ALL) NOPASSWD:ALL
```

## Configure static IP (host-only interface)

```sh
$ ifconfig
$ sudo nano /etc/network/interfaces
```

Add the following configuration (it may differ depending on your interface id):

```
# The hostonly network interface
auto enp0s8
iface enp0s8 inet static
address 192.168.33.10
netmask 255.255.255.0
network 192.168.33.0
broadcast 192.168.33.255
```

Reboot for the changes to take effect:

```sh
$ sudo reboot -h now
```

## Copy public SSH key

Copy the public ssh keys of users that need to have access granted with 
`ssh-copy-id`:

```sh
$ ssh-copy-id -i ~/.ssh/user_id_rsa.pub senaite@192.168.33.10
```

## Setup .ssh/config to make the access easier

```
$ nano ~/.ssh/config
```

Add the following configuration:

```
Host senaite-xenial
  HostName 192.168.33.10
  User senaite
  LocalForward 8000 127.0.0.1:8000
  LocalForward 9001 127.0.0.1:9001
  LocalForward 8080 127.0.0.1:8080
  LocalForward 8081 127.0.0.1:8081
  LocalForward 8082 127.0.0.1:8082
  LocalForward 8083 127.0.0.1:8083
```

Note the following ports:
- 8000: Access to VM's control panel
- 9001: Access to VM's supervisor tool
- 8080: Access to VM's client1
- 8081: Access to VM's client2

## Install required packages

Ansible requires python:

```sh
$ sudo apt-get install -y python byobu
```

## Generate a new RSA key for each private repository

We can use this key to register the VM to a private Github repos to be able to
download source code.

```sh
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/github_bhp.lims
```

## Register the new RSA keys

*NOTE: This step can be skipped, cause is only necessary when managing
(cloning, pulling, etc.) private repositories manually (see section "Setup SSH
for multiple private accounts" below for further info).*

New keys need registered before they are useful. To register, we need to use
ssh-agent and to use that, we need to first make sure it is running:

```sh
$ eval "$(ssh-agent -s)"
```

Once running, you can then add your new keys. Repeat the following command for
all new keys you have added, substituting the correct path to the private key:

```sh
$ ssh-add ~/.ssh/github_bhp.lims
```

## Add SSH keys to Github

Copy&Paste the public key to the private Github's repos. Repeat this process for
all new keys for private Github repositories you've added:

https://github.com/bhp-lims/bhp.lims/settings/keys


## Setup SSH for multiple private Github accounts

GitHub allows you to attach a deploy key to any of your repositories. However,
each repo must have its own unique key.

```sh
$ nano ~/.ssh/config
# ~/.ssh/config

Host github-bhp-lims
HostName github.com
User git
IdentityFile ~/.ssh/github_bhp.lims

$ chmod 600 ~/.ssh/config
```

Ansible recipe is configured to use the following command to clone the repos:

```sh
$ git clone github-bhp-lims:bhp-lims/bhp.lims
```

*See configure.yml*


# Setup the VM with Ansible

Go to `ansible` directory from the add-on and clone `senaite.ansible-playbok`:

```
$ git clone https://github.com/senaite/senaite.ansible-playbook
```

Check all is in place and we are able to reach the VM with ansible

```sh
$ ansible senaite-xenial -i hosts.cfg -m setup
```

Install ansible dependencies

```sh
$ ansible-galaxy install -f -r senaite.ansible-playbook/requirements.yml
```

Run the ansible playbook

```sh
$ ansible-playbook -vv -i hosts.cfg playbook.yml --vault-password-file vault.txt
```

Note `vault.txt` file is not in the repository, and it **never** should!.
