#!/bin/bash

set -e

install_dependencies() {
	if ! docker &> /dev/null
	then
		echo "Installing docker..." && sleep 3
		sudo apt-get update
		sudo apt-get install ca-certificates curl gnupg lsb-release -y
		mkdir -m 0755 -p /etc/apt/keyrings
		curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
		echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
		sudo apt-get update
		sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
		usermod -aG docker $USER
		sudo apt-get clean
	fi

	if ! kubectl &> /dev/null
	then
		echo "Installing kubectl..." && sleep 3
		sudo curl "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" -Lo /usr/local/bin/kubectl
		sudo chmod +x /usr/local/bin/kubectl
	fi

	if ! flytectl &> /dev/null
	then
		echo "Installing flytectl..." && sleep 3
		curl -sL https://ctl.flyte.org/install | sudo bash
		sudo mv ./bin/flytectl /usr/local/bin/
		sudo rm -R ./bin
	fi

	echo "Dependencies installed."
}

deploy() {
	flytectl demo start
}

teardown() {
	flytectl demo teardown
	docker volume rm flyte-sandbox
	. ./.devcontainer/.env && docker run --rm mysql:5.7 mysql -h$DJ_HOST -u$DJ_USER -p$DJ_PASS -e "DROP DATABASE flyte_demo;"
}

"$@"