#! /usr/bin/python3

import math

####################################################
## GLOBAL VARS 
####################################################
L_l = 3
L_s = 3


####################################################
## COORDINATE TRANFORMS 
####################################################

# Cartesian to cylindrical polar coordinates
def cart2cyl(coords):
    x, y, z = coords
    r = math.sqrt(x**2 + y**2 + z**2)
    phi = math.atan2(y/x)
    return r, phi, z

# Cylindrical polar to Cartesian coordinates
def cyl2cart(coords):
    r, phi, z = coords
    x = r*math.cos(phi)
    y = r*math.sin(phi)
    return x, y, z

# Cartesian to spherical polar coordinates
def cart2sph(coords):
    x, y, z = coords
    r = math.sqrt(x**2 + y**2 + z**2)
    theta = math.atan2(y, x)
    phi = math.acos(z / r)
    return r, theta, phi

# Spherical polar to Cartesian coordinates
def sph2cart(coords):
    r, phi, theta = coords
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return


####################################################
## STEERING FUNCTIONS 
####################################################

def lpStart(beta1, beta2, phi):
    """
    For given mirror positions beta1 and beta2, as well as azimuthal rotation phi,
    calculate the (x, y) position wrt the origin at the center of rotation
    
    beta1 --- angle of first mirror wrt beam axis
    beta2 --- angle of second mirror wrt mirror normal
    phi ----- azimuthal rotation of the egg
    """
    
    # set global constants
    D = 1   # distance between lightpipe and first (inner) mirror
    r0 = 1  # distance between first (inner) and second (outer) mirror
    W = 1   # lightpipe width - need to check if initial position exceeds pipe dimension
            
    # calculate angle of incidence 
    theta1 = 2*beta1 - 2*beta2 
    
    # calculate distance from central beam axis
    h = r0*math.sin(2*beta1) - (D + r0*math.cos(2*beta1))*math.tan(theta1)
    if h > W:
        print("Trajectory Error: Initial position exceeds lightpipe aperture dimension.")
    
    # use phi to calculate x and y
    x = h*math.cos(phi)
    y = h*math.sin(phi)
    
    # return Cartesian coordinates of start
    return x, y, theta1



def snellAngle(n1, n2, theta1):
    """
    n1 ------ initial medium index of refraction
    n2 ------ new medium index of refraction
    theta1 -- angle of incidence (in initial medium)
    """
    
    theta2 = math.asin(n1/n2*math.sin(theta1))
    
    return theta2



def reflect(eqn_pln, vec):
    """
    For a plane with equation Ax+By+Cz+D=0 , reflect() the plane normal can be constructed as (A, B, C)
    
    n_pln --- normal vector (n_x, n_y, n_z) orthogonal to plane
    d ------- any point on the plane that satisfies d = -p*N
    vec ----- (v_x, v_y, v_z) 
    """
    
    # first we assign variables
    n_x, n_y, n_z, d = eqn_pln
    v_x, v_y, v_z = vec
    
    # normalize just in case
    n = math.sqrt(n_x**2 + n_y**2 + n_z**2)
    
    # assign unit normal coefficients
    a = n_x/n
    b = n_y/n
    c = n_z/n
    
    # construct initial state vector and reflection matrix
    v = [[v_x], [v_y], [v_z], [1]]
    A = [[1-2*a**2, -2*a*b, -2*a*c, -2*a*d],
         [-2*a*b, 1-2*b**2, -2*b*c, -2*b*d],
         [-2*a*c, -2*b*c, 1-2*c**2, -2*c*d],
         [0, 0, 0, 1]]
    
    # perform matrix transformation
    T = A*v
    
    # extract
    T_x, T_y, T_z = T[0:2]
    
    return T_x, T_y, T_z
    


def makeLine(pt1, pt2):
    """
    not sure if i need this, but just in case, constructs a line from 2 points
    returns vector and intercept
    pt1 --- (x1, y1, z1)
    pt2 --- (x2, y2, z2)
    """
    
    vec = pt2 - pt1
    
    return vec, pt1


def findIntercept(eqn_pln, line_vec, line_pt):
    """
    if i have laser at one position, traveling in a particular direction, where is the next place it
    strikes the quartz bar?
    
    
     
    eqn_pln --- plane of intersection (Ax + By + Cz + D = 0)
    line_vec -- for line (r = r0 + vt), line_vec denotes vector v
    line_pt --- for line, line_pt denotes any point r0 thru which the line travels
    """
    
    # unpack plane normal
    n_pln = []*3
    n_pln[0], n_pln[1], n_pln[2], d = eqn_pln
    
    # check plane normal and vector for line have same dimension
    # also check dot product to ensure vector and plane aren't parallel
    nan = float("nan")
    if len(n_pln) != len(line_vec):
        print("Trajectory Error: Plane or vector has wrong dimension")
        return nan, nan, nan
    if len(line_vec) != len(line_pt):
        print("Trajectory Error: Vector equation has mismatched dimension")
        return nan, nan, nan
    
    ################# THESE LINES NEED HELP #################
    if np.dot(n_pln, line_vec) <= 10^-8:
        print("Trajectory Error: Given plane is parallel to laser trajectory")
        return nan, nan, nan
    ################# THESE LINES NEED HELP #################
    
    # reverse solve for parameterization variable t, then plug into vector line eqn for point
    ################# THESE LINES NEED HELP #################
    t = -(d + np.dot(n_pln, line_pt))/np.dot(n_pln, line_vec)
    x, y, z = line_vec*t + line_pt
    ################# THESE LINES NEED HELP #################
    
    # need to add in software stop for boundaries
        
    return x, y, z



def steer(beta1, beta2, phi, L):
    """
    steer() strings together the functions above
    
    theta --- polar angle (angle of incidence wrt lightpipe surface)
    phi ----- azimuthal rotation angle about the beam axis
    L ------- length of lightpipe
    """
    # GLOBAL CONSTANTS
    n1 = 1
    n2 = 1.3
    D = 1
    W = 1
    plns = [[[1, 0, 0, W/2],
             [0, 1, 0, W/2],
             [-1, 0, 0, W/2],
             [0, -1, 0, W/2],
             [0, 0, 1, L]]]
    
    # run thru lpStart to obtain initial point, start at z=0
    x_init, y_init, theta_init = lpStart(beta1, beta2, phi)
    z = 0
    
    # run theta thru Snell's Law to get new theta
    theta_lp = snellAngle(n1, n2, theta_init)
    
    # compute unit vector components from 
    v_x = math.sin(theta_lp)*math.cos(phi)
    v_y = math.sin(theta_lp)*math.sin(phi) 
    v_z = math.cos(theta_lp)
    v = [v_x, v_y, v_z]
    
    # initialize array for line intercepts
    pos = [[]*1000]*3
    cnt = 0
    
    # iteratively call 
    while z < L:
        
        # create temporary array to store possible intercepts
        pos_temp = [[]*3]*4
        
        # find intersection of laser with each of 4 walls
        pos_temp[0,:] = findIntercept(plns[0,:], v, pos)
        pos_temp[1,:] = findIntercept(plns[1,:], v, pos)
        pos_temp[2,:] = findIntercept(plns[2,:], v, pos)
        pos_temp[3,:] = findIntercept(plns[3,:], v, pos)
        
        # find next z (subtract current z and take smallest positive value
        z_temp = pos_temp[:,2]
        print(z_temp)
        z_temp = z_temp - z
        z_indx = z_temp.index(min([i for i in z_temp if i > 0]))
        
        # reflect to get new vector
        v = reflect(plns[z_indx,:], pos)
         
        # store intercept in array outside loop and increase count
        pos[:,cnt] = pos_temp[z_indx,:]
        cnt = cnt + 1 
    
    return pos