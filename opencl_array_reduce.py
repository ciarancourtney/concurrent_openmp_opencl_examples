import pyopencl as cl
import numpy as np


def run(count):
    # init opencl device (may need to change this if you have multiple devices)
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)
    thread_count = ctx.get_info(cl.context_info.DEVICES)[0].max_work_group_size

    N = 2 ** count  # must be a multiple of thread_count
    array = np.arange(N).astype(np.uint32)
    placeholder = np.empty(thread_count).astype(np.uint32)
    result_sum = np.empty(1).astype(np.uint32)

    mf = cl.mem_flags
    array_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=array)
    placeholder_buf = cl.Buffer(ctx, mf.READ_WRITE, size=placeholder.nbytes)
    result_sum_buf = cl.Buffer(ctx, mf.WRITE_ONLY, size=result_sum.nbytes)
    local_buf = cl.LocalMemory(4 * thread_count)  # each int requires 4 bytes

    # load opencl kernel code from file
    with open('opencl_array_reduce.cl', 'r') as f:
        cl_code = "".join(f.readlines())
    cl_kernel = cl.Program(ctx, cl_code).build()

    evt = cl_kernel.reduce(queue, (N,), (thread_count,), array_buf, placeholder_buf, local_buf)
    evt.wait()
    t1 = 1e-10 *(evt.profile.end - evt.profile.start)

    evt = cl_kernel.reduce(queue, (thread_count,), (thread_count,), placeholder_buf, result_sum_buf, local_buf)
    evt.wait()
    t2 = 1e-10 *(evt.profile.end - evt.profile.start)
    cl.enqueue_copy(queue, result_sum, result_sum_buf)

    #print(result_sum, np.sum(array))  # uncomment to compart actual with opencl kernel result

    # return total time taken in seconds
    return (t1+t2)
