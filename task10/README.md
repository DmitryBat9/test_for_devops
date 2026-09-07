# Задание 10 — безопасность Kubernetes

Задание выполнено поверх кластера из задания 9. В кластере установлены:

- Cilium 1.20.1 вместо Flannel;
- Istio 1.31.0 с CNI и отдельным ingress gateway;
- OPA Gatekeeper 3.23.1.

Компоненты установлены официальными Helm charts. В репозитории не дублируются
их большие upstream-манифесты: здесь хранятся настройки, относящиеся к заданию.

## Что ограничено

`cilium/task9-egress-policy.yaml` разрешает Pod приложения обращаться к
ресурсам кластера и выполнять требуемый заданием ICMP ping до `77.88.8.8`.
Остальной внешний трафик блокируется.

Манифесты в `istio` включают строгий mTLS, запрещают прямой доступ к приложению
и разрешают запросы только от service account ingress gateway. Внешний HTTP
доступ настроен через `task9.local:30081`.

В `gatekeeper` находятся квоты namespace и три admission-ограничения:

- максимальные ресурсы контейнера — `300m` CPU и `300Mi` памяти;
- корневая файловая система контейнера должна быть read-only;
- приложение должно запускаться с UID/GID `10001`.

Образ Istio Proxy исключён из проверок UID/GID и лимита `300m`, потому что у
него собственный пользователь и собственные ресурсы.

## Применение политик

```bash
bash task10/gatekeeper/install-templates.sh
kubectl apply -f task10/gatekeeper/namespace-resources.yaml
kubectl apply -f task10/istio/
kubectl apply -f task10/cilium/
kubectl apply -f task10/gatekeeper/constraints.yaml
```

Скрипт `install-templates.sh` устанавливает официальные ConstraintTemplate из
Gatekeeper Library.

## Проверка

```bash
cilium status --wait
kubectl -n istio-system get pods
kubectl -n istio-ingress get pods,service
kubectl -n task9 get pods
kubectl get k8scontainerlimits,k8spspreadonlyrootfilesystem,k8spspallowedusers
curl -i -H 'Host: task9.local' http://192.168.50.22:30081/health
```

Итоговая проверка: обе реплики приложения имели статус `2/2 Running`, запрос
через gateway возвращал `200 OK`, а тестовый Pod с нарушениями был отклонён
Gatekeeper при `kubectl apply --dry-run=server`.
