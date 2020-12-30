# Nibbler Operator

A Kubernetes Operator which facilitates the Nibbler pattern.

# Nibbler Pattern
The Nibbler pattern is designed for long running jobs comprised of very small incremental tasks (or, "nibbles"). 
There are 4 total components in the pattern, 3 are "stock" and 1 is to be provided by the developer.

## Components

### 1. Custom Worker
For each type of job, create a worker. This is an HTTP server with a few key endpoints. 
One for "init", which is used to create the list of nibbles (for job tracking), and one
for completing/performing a specific task/nibble.

### 2. The Vendor
A stock component which vends out individual nibbles, with status tracking. Encapsulates a database for job tracking.

### 3. The Broker
Pulls from vendor and Pushes to Worker. This component exists to simplify the interface of custom component. 
Following in the Framework tradition of "Don't call us, we'll call you", this component consumes the HTTP interface of the custom worker.
The broker is essentially an infinite loop like this:
```
while(tasks =  get_task_from_vendor())
    send_task_to_worker(task)
````

### 4. This Operator
This operator distills the pattern to a Kubernetes CRD (custom resource definition), in which the user specifies only the worker image (and optionally, some env/config).
Upon creation, it will launch a pod with a broker + worker into the namespace of the Custom Resource and kicks off processing. 