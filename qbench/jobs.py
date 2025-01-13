"""Implementation of utilities for interacting with jobs."""
from functools import singledispatch
from typing import Sequence

from qiskit.providers import JobV1
from qiskit_ibm_provider import IBMProvider
#from qiskit.providers.ibmq import IBMQBackend, IBMQJob
from qiskit_ibm_runtime import QiskitRuntimeService
import os


# TODO IBMQ_TOKEN is deprecated by now
IBMQ_TOKEN = os.getenv('IBMQ_TOKEN')
QISKIT_IBM_TOKEN = os.getenv('QISKIT_IBM_TOKEN')

# TODO Maybe stop supporting IBMQ_TOKEN variable?
if sum(e in os.environ for e in ('QISKIT_IBM_TOKEN', 'IBMQ_TOKEN')) == 0:
    raise ValueError('Missing IBM API token! You need to specify it via environment variable QISKIT_IBM_TOKEN or '
                     'IBMQ_TOKEN (deprecated)!')
elif 'IBMQ_TOKEN' in os.environ and not 'QISKIT_IBM_TOKEN' in os.environ:
    QISKIT_IBM_TOKEN = IBMQ_TOKEN

service = QiskitRuntimeService('ibm_quantum', QISKIT_IBM_TOKEN)

@singledispatch
def retrieve_jobs(job_ids: Sequence[str]) -> Sequence[JobV1]:
    """Retrieve jobs with given ids from a service.

    :param job_ids: identifiers of jobs to obtain.
    :return: sequence of jobs. Note that it is not guaranteed that the order of this sequence
     will match order of ids in job_ids parameter.
    """

    return [service.job(job_id) for job_id in job_ids]


#@retrieve_jobs.register
#def _retrieve_jobs_from_ibmq(backend: IBMQBackend, job_ids: Sequence[str]) -> Sequence[IBMQJob]:
#return backend.jobs(db_filter={"id": {"inq": job_ids}}, limit=len(job_ids))
