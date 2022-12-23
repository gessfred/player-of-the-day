# React template

Create react app starter with CI/CD to deploy and serve the website on Kubernetes.

## Instructions

If not done already, make sure to create a K8s cluster, get an API token to get the kubeconfig, and add imagepullsecrets to the cluster.

1. Add `REGISTRY_TOKEN` and `DIGITAL_OCEAN_TOKEN` to GitHub secrets.
2. Review Dockerfile
3. Fix name of deployment and svc in K8s manifest
4. Fix names in the GitHub action
5. Enable workflow by adding branches on push
