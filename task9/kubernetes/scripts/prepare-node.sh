#!/usr/bin/env bash

set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
    echo "Run this script with sudo: sudo bash prepare-node.sh" >&2
    exit 1
fi

export DEBIAN_FRONTEND=noninteractive

echo "[1/7] Disabling swap"
swapoff --all
sed -ri '/[[:space:]]swap[[:space:]]/s/^#?/#/' /etc/fstab

echo "[2/7] Loading kernel modules"
cat >/etc/modules-load.d/kubernetes.conf <<'EOF'
overlay
br_netfilter
EOF
modprobe overlay
modprobe br_netfilter

echo "[3/7] Applying networking sysctl parameters"
cat >/etc/sysctl.d/99-kubernetes.conf <<'EOF'
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward = 1
EOF
sysctl --system >/dev/null

echo "[4/7] Installing containerd and repository prerequisites"
apt-get update
apt-get install --yes apt-transport-https ca-certificates containerd curl gpg

echo "[5/7] Configuring containerd with the systemd cgroup driver"
install -d -m 0755 /etc/containerd
containerd config default >/etc/containerd/config.toml
sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
systemctl enable --now containerd
systemctl restart containerd

echo "[6/7] Adding the Kubernetes 1.36 package repository"
install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.36/deb/Release.key \
    | gpg --dearmor --yes -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
chmod 0644 /etc/apt/keyrings/kubernetes-apt-keyring.gpg
cat >/etc/apt/sources.list.d/kubernetes.list <<'EOF'
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.36/deb/ /
EOF

echo "[7/7] Installing and holding kubelet, kubeadm and kubectl"
apt-get update
apt-get install --yes kubelet kubeadm kubectl
apt-mark hold kubelet kubeadm kubectl
systemctl enable kubelet

sed -ri '/^127\.0\.1\.1[[:space:]]+task9-k8s-(cp|w1|w2)([[:space:]]|$)/d' /etc/hosts

if ! grep -q '^# Task 9 Kubernetes nodes$' /etc/hosts; then
    cat >>/etc/hosts <<'EOF'

# Task 9 Kubernetes nodes
192.168.50.21 task9-k8s-cp
192.168.50.22 task9-k8s-w1
192.168.50.23 task9-k8s-w2
EOF
fi

echo
echo "Node preparation completed."
echo "Swap devices (the output must be empty):"
swapon --show
echo
containerd --version
kubeadm version -o short
kubelet --version
kubectl version --client
systemctl is-active containerd
