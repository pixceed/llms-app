# LLMs-APP

## Docker 環境構築

### プロキシ無し

イメージ作成

``` bash
docker build -t llms_app_image:1.0 build
```

コンテナ作成

``` bash
docker run -it -v `pwd`:/home/ubuntu/workspace -p 8511:8511 --name llms_app_container llms_app_image:1.0 bash
```

### プロキシあり

イメージ作成

``` bash
 docker build --no-cache --force-rm=true \
    --build-arg http_proxy=[PROXY] \
    --build-arg https_proxy=[PROXY] \
    -t llms_app_image:3.0 \
    build
```

コンテナ作成

``` bash
docker run -it \
    -v `pwd`:/home/ubuntu/workspace \
    --env HTTP_PROXY=[PROXY] \
    --env HTTPS_PROXY=[PROXY] \
    -p 8512:8512 \
    --name llms_app_container llms_app_image:3.0 bash
```
