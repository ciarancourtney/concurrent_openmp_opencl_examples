__kernel void reduce(__global int *a, __global int *r, __local int *b) {
    uint global_id = get_global_id(0);
    uint group_id = get_group_id(0);
    uint local_id = get_local_id(0);
    uint local_size = get_local_size(0);

    b[local_id] = a[global_id];
    barrier(CLK_LOCAL_MEM_FENCE);

    for(uint s = local_size/2; s > 0; s >>= 1) {
    if(local_id < s) {
      b[local_id] += b[local_id+s];
    }
    barrier(CLK_LOCAL_MEM_FENCE);
    }
    if(local_id == 0) r[group_id] = b[local_id];
}
