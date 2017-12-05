# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.help_files import helps

helps['acs'] = """
     type: group
     short-summary: Manage Azure Container Services.
"""
helps['acs dcos'] = """
    type: group
    short-summary: Manage a DC/OS orchestrated Azure Container Service.
"""
helps['acs kubernetes'] = """
    type: group
    short-summary: Manage a Kubernetes orchestrated Azure Container Service.
"""
helps['acs kubernetes get-credentials'] = """
    type: command
    short-summary: Download and install credentials to access a cluster.
"""
helps['acs scale'] = """
    type: command
    short-summary: Change the private agent count of a container service.
"""
helps['acs install-cli'] = """
    type: command
    short-summary: Download and install the DC/OS and Kubernetes command line for a cluster.
"""
helps['acs create'] = """
    type: command
    short-summary: Create a new Azure Container Service cluster.
    examples:
        - name: Create a default acs cluster.
          text: az acs create -g MyResourceGroup -n MyContainerService
        - name: Create a Kubernetes cluster.
          text: az acs create --orchestrator-type Kubernetes -g MyResourceGroup -n MyContainerService
        - name: Create a Kubernetes cluster with a an existing SSH key.
          text: az acs create --orchestrator-type Kubernetes -g MyResourceGroup -n MyContainerService --ssh-key-value /path/to/publickey
        - name: Create an ACS cluster with two agent pools.
          text: az acs create -g MyResourceGroup -n MyContainerService --agent-profiles "[{'name':'agentpool1'},{'name':'agentpool2'}]"
        - name: Create an ACS cluster where the second agent pool has a vmSize specified.
          text: az acs create -g MyResourceGroup -n MyContainerService --agent-profiles "[{'name':'agentpool1'},{'name':'agentpool2','vmSize':'Standard_D2'}]"
        - name: Create an ACS cluster with agent-profiles specified from a file.
          text: az acs create -g MyResourceGroup -n MyContainerService --agent-profiles MyAgentProfiles.json
"""
helps['aks'] = """
     type: group
     short-summary: Manage Kubernetes clusters.
"""
helps['aks create'] = """
    type: command
    short-summary: Create a new Azure managed Kubernetes cluster.
    examples:
        - name: Create a Kubernetes cluster.
          text: az aks create -g MyResourceGroup -n MyManagedCluster
        - name: Create a Kubernetes cluster with a an existing SSH key.
          text: az aks create -g MyResourceGroup -n MyManagedCluster --ssh-key-value /path/to/publickey
        - name: Create a Kubernetes cluster with a specific version
          text: az aks create -g MyResourceGroup -n MyManagedCluster --kubernetes-version 1.8.1
        - name: Create a Kubernetes cluster with a larger node pool count
          text: az aks create -g MyResourceGroup -n MyManagedCluster --node-count 7
"""
helps['aks delete'] = """
    type: command
    short-summary: Delete a managed Kubernetes cluster.
"""
helps['aks get-versions'] = """
    type: command
    short-summary: Get versions available to upgrade a managed Kubernetes cluster.
"""
helps['aks install-cli'] = """
    type: command
    short-summary: Download and install kubectl, the Kubernetes command line tool.
"""
helps['aks wait'] = """
    type: command
    short-summary: Wait for a Kubernetes cluster to reach a desired state.
"""
helps['aks install-connector'] = """
    type: command
    short-summary: Deploy the ACI-Connector to a AKS cluster.
    examples:
        - name: Install the ACI-Connector to an AKS Cluster.
          text: az aks install-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector
        - name: Install the ACI-Connector for Windows to an AKS Cluster.
          text: az aks install-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector --os-type Windows
        - name: Install the ACI-Connector for Windows and Linux to an AKS Cluster.
          text: az aks install-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector --os-type Both
        - name: Install the ACI-Connector using specific SPN.
          text: az aks install-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector --service-principal <SPN_ID> --client-secret <SPN_SECRET>
        - name: Install the ACI-Connector from a specific custom chart.
          text: az aks install-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector --chart-url <CustomURL>
"""
helps['aks remove-connector'] = """
    type: command
    short-summary: Undeploy the ACI-Connector from an AKS cluster.
    examples:
        - name: Undeploy the ACI-Connector on an AKS cluster.
          text: az aks remove-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector
        - name: Undeploy the ACI-Connector on an AKS cluster using the graceful mode
          text: az aks remove-connector --name MyManagedCluster --resource-group MyResourceGroup --connector-name MyConnector --graceful
"""
