# Aspecta – Kubernetes infraštruktúra

Frontend (Nginx) a backend (FastAPI) bežia v minikube. Nasadenie aplikácie spravuje Argo CD pomocou Helm chartu. GitHub Actions zostavujú Docker images, publikujú ich do GHCR a pripravujú aktualizáciu chartu. Monitoring tvorí Prometheus a Alertmanager.

## 1. Dizajn riešenia


Používateľ → Ingress (aspecta.local)
               ├─ /     → frontend-service:80 → frontend:80
               └─ /api  → backend-service:8000 → backend:8000

GitHub Actions → GHCR images + Helm balík
               → PR s novým image tagom → merge do main → Argo CD


## 2. Predpoklady a príprava repozitára

Docker, minikube, kubectl, helm, git


## 3. Inštalácia Argo CD

kubectl create namespace argocd 
kubectl apply --server-side -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.4/manifests/install.yaml


## 4. Nasadenie aplikácie a monitoringu

kubectl --context minikube apply -f argocd/application.yaml
kubectl --context minikube apply -f argocd/monitoring.yaml
kubectl --context minikube -n argocd get applications -w

Počkaj na `Synced` a `Healthy` pri `aspecta` aj `monitoring`, potom ukonči sledovanie cez Ctrl+C. Prvé sťahovanie images a inštalácia monitoringu môžu trvať niekoľko minút.


## 5. Monitoring a alerty

Stack obsahuje Prometheus Operator, Prometheus, Alertmanager, kube-state-metrics a node exporter. Sleduje Kubernetes stav aplikácie; aplikácia neexportuje vlastné HTTP metriky. Grafana je vypnutá. Dáta sú dočasné, retention Promethea je 24 hodín.


## 6. Ďalšie zmeny a CI/CD

1. Zmena `app/backend` alebo `app/frontend` spustí príslušný GitHub workflow.
2. Pipeline zostaví image a publikuje ho do GHCR s tagom odvodeným od commit SHA.
3. Aktualizuje image tag v Helm values, vykoná lint, render a `helm package`.
4. Balík `.tgz` uloží v **Actions → konkrétny beh → Artifacts** ako `aspecta-backend-chart` alebo `aspecta-frontend-chart`.
5. Vytvorí PR s aktualizovaným image tagom. Po merge do `main` Argo zmenu automaticky nasadí.

Argo používa chart priamo z Gitu; CI balík sa nepublikuje do GHCR a nie je zdrojom tohto nasadenia. Verzia balíka obsahuje komponent a číslo behu, zdrojový `Chart.yaml` sa nemení.
