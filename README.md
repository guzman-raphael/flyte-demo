## Flyte Demo


![screenshot of flyte workflow success](./screenshots/wf_success.png "Flyte Workflow")

### Outline

1. Use Case & Limitations
1. Definitions
1. Launching Workflows
1. Successful Workflow
1. Failed Workflow

### Instructions

1. Setup and configure MySQL RDS
   - deployed on aws + add sg rule for port 3306 that should be removed later
1. Add DataJoint env vars to `./.devcontainer/.env`
1. Run `./sandbox.sh install_dependencies` locally
1. Run `./sandbox.sh deploy` locally
1. ```bash
   # prepare task environment (replace all `raphaelguzman` with DockerHub user)
   docker login
   docker build . -t raphaelguzman/flyte-demo-task:v0.1.4
   docker push raphaelguzman/flyte-demo-task:v0.1.4
   ```
1. Launch `Demo` DevContainer
1. ```bash
   # register workflow
   pyflyte register --project flytesnacks --domain development src/workflow_v4.py
   ```
1. ```bash
   # run workflow
   pyflyte run --remote --project flytesnacks --domain development src/workflow_v4.py flow1 --session_rows '[{"session_id": 0}]' --parameter_rows '[{"param_id": 0, "param_a": 5, "param_b": 8}]'
   ```
1. Explore Console at `http://localhost:30080/console`

### Teardown

1. Close `Demo` DevContainer
1. `./sandbox.sh teardown`

### Debug

Run the following in `Demo` DevContainer to:

- Explore database server
  ```bash
  mysql -h$DJ_HOST -u$DJ_USER -p$DJ_PASS
  ```
