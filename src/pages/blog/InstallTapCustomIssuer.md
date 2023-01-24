---
layout: $/layouts/post.astro
title: "Creating a Custom ClusterIssuer using a Private Certificate Authority for a Tanzu Application Platform 1.4 Installation"
description: "Watch me interact with ChatGPT as it provides nuanced and detailed responses helping me configure a private self-signed CA for my Tanzu Application Platform, Kubernetes (minikube) and Harbor lab" 
# there MUST be at least 1 tag listed or it will not render
tags:
  - Tanzu
  - "Tanzu Application Platform"
  - "Cert-Manager"
  - "Platform Engineering"
  - Kubernetes
  - "Tanzu Packages"
  - "Certificates"
  - "Private Certificate Authority"
  - OvaTheTap
author: Art Fewell
authorTwitter: afewell
date: 2023-1-23T08:00:18.276Z
---

Tanzu Application Platform (TAP) 1.4 installs cert-manager by default. The default installation of cert-manager is a pretty standard installation, and if you have used cert-manager before, using the cert-manager instance installed with TAP is essentially identical. 

As you would with any cert-manager installation, after install, you create issuers that can provision certificates upon request, based on various criteria. 

I am working on my [ovathetap](https://github.com/afewell/ovathetap) project where I am continuing to refine my single node TAP environment, and wanted to update my installation flow to use a issuer based on the private certificate authority (CA) I have setup in my lab environment. 

If you are interested, [you can view the script I use to setup my private CA here](https://github.com/afewell/ovathetap/blob/main/scripts/certificateauthority.sh)

Fortunately, the [documentation](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.4/tap/tap-gui-tls-cert-mngr-ext-clusterissuer.html?hWord=N4IghgNiBcIMYFMBOAXAtAWzAOzAc2QAIEAPFZXKAXyA) about how to setup issuers for TAP environments is great - but I did do some customization beyond the standard method.

The standard procedure for cert-manager setup is:
1. Install TAP which includes cert-manager installation
2. Install a standard issuer or clusterIssuer using any method supported on the version of cert-manager installed. TAP uses a standard distribution of cert-manager with no special restrictions or requirements. 
3. Insert an annotation in your deployments specifying the name of your issuer
4. If you also want TAP UI components to use your issuer, add a shared.ingress_issuer key to your tap-values.yaml file and update your tap install. 

While the standard procedure works perfectly well, I wanted to try doing it a little differently. I don't have any meaningful reason other than personal preference, but I wanted to try to setup this flow so that the TAP installation uses my private CA from its initial installation, rather than adding the issuer and then updating the installation. 

One way of accomplishing this would be to do a tradition cert-manager installation before the tap install, and then just specify the issuer in the tap-values file for the initial installation. And I am sure this would work perfectly well, but I dont know if there is anything extra I would need to do to have TAP integrate with a previously installed cert-manager, or if I would need to exclude cert-manager from the tap install to prevent collisions ... I didnt try, and I dont know if or what configuration may be needed, but to avoid that question, I thought I would try a different path ... install cert-manager before TAP, but do so using the tanzu package for cert-manager from the same TAP installation environment, just before you actually install TAP. And it turns out, this method is [well documented](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.4/tap/cert-manager-install.html).

So my modified tap installation workflow follows the [standard install documentation] up to the point where you create the tap-install namespace and install the tap-registry and tap-repository, but before I actually do the tap install I do the following:
1. Install the tanzu package for cert-manager using the [instructions from the TAP documentation](https://docs.vmware.com/en/VMware-Tanzu-Application-Platform/1.4/tap/cert-manager-install.html).
```sh
# create cert-manager-rbac.yaml and cert-manager-install.yaml files per the documentation
# Create cert-manager namespace
kubectl create ns cert-manager
# create cert-manager cluster role and service account
kubectl apply -f cert-manager-rbac.yaml
# Install cert-manager
kubectl apply -f "/${ovathetap_home}/config/cert-manager-install.yaml"
```
2. Create a secret using your private CA cert and key files (This example specifies the location where my CA files are stored on the host that is executing the kubectl command)
```sh
kubectl create secret tls my-ca-secret --key /etc/ssl/CA/myca.key --cert /etc/ssl/CA/myca.pem -n cert-manager
```
3. Create a ClusterIssuer using the secret with your private CA tls data
```sh
# Create clusterIssuer yaml file based on lab CA cert secret
cat << EOF > my-ca-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: my-ca-issuer
  namespace: cert-manager
spec:
  ca:
    secretName: my-ca-secret
EOF
# Create the ClusterIssuer with the following command
kubectl apply -f my-ca-issuer.yaml -n cert-manager
# Verify the cluster issuer was created and is ready with the following command:
kubectl get ClusterIssuer
```
4. Update your tap values file so it uses your issuer. Note, you still should include your private ca cert in the shared.ca_cert_data value because it is used for different purposes.
```sh
 #tap-values.yaml
 shared:
  ingress_domain: "tanzu.demo"
  ingress_issuer: "my-ca-issuer" # Optional, can denote a cert-manager.io/v1/ClusterIssuer of your choice. Defaults to "tap-ingress-selfsigned".

  image_registry: 
    project_path: "https://harbor.tanzu.demo/tap"
    username: "admin"
    password: "Harbor12345"
  ca_cert_data: |
      -----BEGIN CERTIFICATE-----
    MIIFvTCCA6WgAwIBAgIUdquZ8e8rKrE0Mt3w1M/Cc6sYXZYwDQYJKoZIhvcNAQEN
    BQAwbjELMA<<<<           REDACTED                >>>>DAOBgNVBAcM
    P38lHwHbzcLmvXamhE37gqd9mQPoykfjashflsdalfjsldf93j8T9xRY7h108wnZ
    -----END CERTIFICATE-----

ceip_policy_disclosed: true # Installation fails if this is not set to true. Not a string.

profile: full # Can take iterate, build, run, view.

supply_chain: basic # Can take testing, testing_scanning.
```
5. Install TAP
```sh
tanzu package install tap -p tap.tanzu.vmware.com -v $TAP_VERSION --values-file tap-values.yaml -n tap-install
```

My environment is already setup to trust my private CA, so after the tap installation completed, I was able to immediately go to my tap-gui URL with no alarms as it used a certificate that was provisioned based on my private CA. 

I hope this is useful for you! Thanks for reading!
