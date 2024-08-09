sudo pluginctl deploy \
  --name capture-and-describe-plugin  \
  --develop \
  --entrypoint /bin/bash \
  --selector zone=core \
  --resource request.cpu=2000m,request.memory=3Gi,limit.memory=5Gi \
  10.31.81.1:5000/local/capture-and-describe-plugin \
  -- -c "while true; do sleep 1; done"