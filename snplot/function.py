import numpy as np
from copy import deepcopy
from scipy.interpolate import interp1d
from scipy import signal

def interpolate_data(x, y, jump):
    x_min = int(min(x) // jump)
    x_max = int(max(x) // jump)
    x_new = np.arange(x_min, x_max + 1) * jump
    f = interp1d(x, y)
    y_new = f(x_new)
    return x_new, y_new

def interpolate_data_xbase(x, y, xbase):
    f = interp1d(x, y, fill_value='extrapolate')
    y_new = f(xbase)
    return y_new

def rcparams_predeal(rcparams, scale):
    return_rcparams = {}
    for key in rcparams.keys():
        if "snplot" in key:
            continue
        return_rcparams[key] = rcparams[key]
        if type(rcparams[key]) == int or type(rcparams[key]) == float:
            if 'alpha' in key: continue
            return_rcparams[key] *= scale
    return return_rcparams

def rcparams_update(rc_, rc_u):
    rc_d = deepcopy(rc_)
    for key in rc_u.keys():
        if key in rc_d.keys():
            rc_d[key] = rc_u[key]
    return rc_d

def rcparams_combine(rc_1, rc_2):
    # rc_2 will overwrite rc_1
    rc_d = deepcopy(rc_1)
    for key in rc_2.keys():
        rc_d[key] = rc_2[key]
    return rc_d

def convert_config(args):
    if "xlim" in args.keys():
        args['xlim'] = tuple(args['xlim'])
    if "ylim" in args.keys():
        args['ylim'] = tuple(args['ylim'])
    if "figure.figsize" in args.keys():
        args['figure.figsize'] = tuple(args['figure.figsize'])
    return args

def Euler_trans(euler_vector, axis = 'z'):
    # Transform Euler angle (ZXZ) to rotation matrix
    euler_vector = euler_vector / 180 * np.pi

    SPH=np.sin(euler_vector[0]); CPH=np.cos(euler_vector[0])
    STH=np.sin(euler_vector[1]); CTH=np.cos(euler_vector[1])
    STM=np.sin(euler_vector[2]); CTM=np.cos(euler_vector[2])
    
    if axis=='x':
        return np.array([CTM*CPH-SPH*STM*CTH,-STM*CPH-SPH*CTM*CTH,SPH*STH])
    if axis=='y':
        return np.array([CTM*SPH+CPH*STM*CTH,-SPH*STM+CPH*CTM*CTH,-STH*CPH])
    if axis=='z':
        return np.array([STH*STM,CTM*STH,CTH])
    else:
        matrix = np.array([[CTM*CPH-SPH*STM*CTH,-STM*CPH-SPH*CTM*CTH,SPH*STH],
              [CTM*SPH+CPH*STM*CTH,-SPH*STM+CPH*CTM*CTH,-STH*CPH],
              [STH*STM,CTM*STH,CTH]]).transpose()
        return np.dot(matrix, axis)

def trans_to_xy(axis_vec):
    if axis_vec[2] < 0:
        axis_vec = -axis_vec
    axis_vec = axis_vec.reshape(-1)
    axis_temp = axis_vec - np.array([0,0,-1])
    axis_temp = axis_temp / abs(axis_temp[2])
    return axis_temp - np.array([0,0,1])

def calc_ipf(axis_vec):
    axis_vec = axis_vec/np.linalg.norm(axis_vec)
    sorted_axis = np.sort(np.abs(axis_vec),)
    axis_ipf = np.array([sorted_axis[1],sorted_axis[0],sorted_axis[2]])
    return axis_ipf

def spherical_triangle_area(v1, v2, v3):
    """使用Girard公式计算单位球面三角形面积"""
    # 输入应为单位向量
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    v3 = v3 / np.linalg.norm(v3)
    
    # 计算三个顶点处的内角
    def vertex_angle(center, p1, p2):
        vec1 = p1 - center * np.dot(center, p1)
        vec2 = p2 - center * np.dot(center, p2)
        vec1 /= np.linalg.norm(vec1)
        vec2 /= np.linalg.norm(vec2)
        return np.arccos(np.clip(np.dot(vec1, vec2), -1, 1))
    
    alpha = vertex_angle(v1, v2, v3)
    beta = vertex_angle(v2, v3, v1)
    gamma = vertex_angle(v3, v1, v2)
    
    # Girard公式
    return (alpha + beta + gamma - np.pi)

def spherical_triangle_area_vectorized(v1, v2, v3):
    """
    处理输入形状为 (3, N, N) 的向量化版本
    返回形状为 (N, N) 的面积矩阵
    """
    # 输入形状验证
    assert v1.shape == v2.shape == v3.shape, "输入形状必须一致"
    assert v1.shape[0] == 3, "第一个维度应为三维坐标"

    # 转换维度顺序 (3, N, N) → (N, N, 3)
    def transpose_dims(arr):
        return np.moveaxis(arr, 0, -1)  # 将第0轴移到最后
    
    v1_t = transpose_dims(v1)
    v2_t = transpose_dims(v2)
    v3_t = transpose_dims(v3)

    # 批量归一化函数 (处理(N,N,3)形状)
    def batch_normalize(vec):
        norm = np.linalg.norm(vec, axis=-1, keepdims=True)
        norm = np.where(norm < 1e-12, 1e-12, norm)  # 防止除零
        return vec / norm

    # 归一化处理
    v1_norm = batch_normalize(v1_t)
    v2_norm = batch_normalize(v2_t)
    v3_norm = batch_normalize(v3_t)

    # 向量化角度计算核心函数
    def vectorized_angle(centers, p1s, p2s):
        """ centers, p1s, p2s 形状均为 (N,N,3) """
        # 计算投影向量 (Gram-Schmidt正交化)
        proj_p1 = p1s - np.sum(centers * p1s, axis=-1, keepdims=True) * centers
        proj_p2 = p2s - np.sum(centers * p2s, axis=-1, keepdims=True) * centers
        
        # 归一化投影向量
        proj_p1 = batch_normalize(proj_p1)
        proj_p2 = batch_normalize(proj_p2)
        
        # 计算点积并保证数值稳定性
        dots = np.sum(proj_p1 * proj_p2, axis=-1)
        return np.arccos(np.clip(dots, -1.0 + 1e-12, 1.0 - 1e-12))

    # 计算三个内角 (每个结果形状为(N,N))
    alpha = vectorized_angle(v1_norm, v2_norm, v3_norm)
    beta = vectorized_angle(v2_norm, v3_norm, v1_norm)
    gamma = vectorized_angle(v3_norm, v1_norm, v2_norm)

    # 应用Girard公式并处理退化三角形
    area = alpha + beta + gamma - np.pi
    area = np.where(area < 0, 0, area)  # 处理浮点误差导致的负面积
    
    return area

def get_alignment(pos='u'):
    if pos == 'u' or pos == 'upper':
        return {'ha':'center', 'va':'bottom', 'offset':(0,1)}
    elif pos == 'b' or pos == 'bottom':
        return {'ha':'center', 'va':'top', 'offset':(0,-1)}
    elif pos == 'l' or pos == 'left':
        return {'ha':'right', 'va':'center', 'offset':(-1,0)}
    elif pos == 'r' or pos == 'right':
        return {'ha':'left', 'va':'center', 'offset':(1,0)}
    elif pos == 'ul' or pos == 'upper left':
        return {'ha':'right', 'va':'bottom', 'offset':(-0.7,0.7)}
    elif pos == 'ur' or pos == 'upper right':
        return {'ha':'left', 'va':'bottom', 'offset':(0.7,0.7)}
    elif pos == 'bl' or pos == 'bottom left':
        return {'ha':'right', 'va':'top', 'offset':(-0.7,-0.7)}
    elif pos == 'br' or pos == 'bottom right':
        return {'ha':'left', 'va':'top', 'offset':(0.7,-0.7)}
    else:
        return {'ha':'center', 'va':'center', 'offset':(0,0)}

def add_text(ax, text, x, y, pos = 'u', **kwargs):
    alignment = get_alignment(pos)
    x_scale = max(0.01*x, 0.002)
    y_scale = max(0.01*y, 0.002)
    ax.text(x+x_scale * alignment['offset'][0], y+y_scale * alignment['offset'][1], text, ha=alignment['ha'], va=alignment['va'], **kwargs)
    return ax

def generate_diffusion_kernel(bin_width, physical_sigma, max_kernel_size=21):
    """
    生成自适应高斯扩散核
    
    参数：
    bin_width : float - 网格单元物理尺寸（单位：mm/°等）
    physical_sigma : float - 期望的物理弥散程度（与bin_width相同单位）
    max_kernel_size : int - 最大允许的核尺寸（奇数）

    返回：
    kernel : 2D array - 归一化的高斯核
    """
    # 计算像素空间的sigma
    sigma_pixels = physical_sigma / bin_width
    
    # 自动确定核尺寸（3σ原则，且保持奇数）
    kernel_size = min(2 * int(3 * sigma_pixels) + 1, max_kernel_size)
    kernel_size = max(kernel_size, 3)  # 最小3x3
    
    # 生成高斯核原型
    x = np.linspace(-3, 3, 1000)
    gauss = np.exp(-x**2/(2*sigma_pixels**2))
    
    # 重采样到目标核尺寸
    kernel = signal.resample(gauss, kernel_size)
    
    # 生成2D核并归一化
    kernel_2d = np.outer(kernel, kernel)
    kernel_2d /= kernel_2d.sum()
    
    return kernel_2d
