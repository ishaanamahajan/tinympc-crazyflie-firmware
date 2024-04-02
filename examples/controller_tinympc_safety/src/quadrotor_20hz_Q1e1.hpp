#pragma once

#include <tinympc/types.hpp>

static const tinytype rho_value = 1.0;

static const tinytype Adyn_data[NSTATES*NSTATES]  = {
	1.000000f, 0.000000f, 0.000000f, 0.050000f, 0.000000f, 0.000000f, 
	0.000000f, 1.000000f, 0.000000f, 0.000000f, 0.050000f, 0.000000f, 
	0.000000f, 0.000000f, 1.000000f, 0.000000f, 0.000000f, 0.050000f, 
	0.000000f, 0.000000f, 0.000000f, 1.000000f, 0.000000f, 0.000000f, 
	0.000000f, 0.000000f, 0.000000f, 0.000000f, 1.000000f, 0.000000f, 
	0.000000f, 0.000000f, 0.000000f, 0.000000f, 0.000000f, 1.000000f
};

static const tinytype Bdyn_data[NSTATES*NINPUTS]  = {
	0.001250f, 0.000000f, 0.000000f, 
	0.000000f, 0.001250f, 0.000000f, 
	0.000000f, 0.000000f, 0.001250f, 
	0.050000f, 0.000000f, 0.000000f, 
	0.000000f, 0.050000f, 0.000000f, 
	0.000000f, 0.000000f, 0.050000f
};

static const tinytype fdyn_data[NSTATES]  = {0.000000f, 0.000000f, -0.012263f, 0.000000f, 0.000000f, -0.490500f};

static const tinytype Q_data[NSTATES] = {11.000000f, 11.000000f, 11.000000f, 11.000000f, 11.000000f, 11.000000f};

static const tinytype R_data[NINPUTS] = {2.000000f, 2.000000f, 2.000000f};

static const tinytype Kinf_data[NINPUTS*NSTATES]  = {
	2.165405f, 0.000000f, 0.000000f, 3.003297f, 0.000000f, 0.000000f, 
	0.000000f, 2.165405f, 0.000000f, 0.000000f, 3.003297f, 0.000000f, 
	0.000000f, 0.000000f, 2.165405f, 0.000000f, 0.000000f, 3.003297f
};

static const tinytype Pinf_data[NSTATES*NSTATES]  = {
	305.127753f, 0.000000f, 0.000000f, 93.969410f, 0.000000f, 0.000000f, 
	0.000000f, 305.127753f, 0.000000f, 0.000000f, 93.969410f, 0.000000f, 
	0.000000f, 0.000000f, 305.127753f, 0.000000f, 0.000000f, 93.969410f, 
	93.969410f, 0.000000f, 0.000000f, 133.481105f, 0.000000f, 0.000000f, 
	0.000000f, 93.969410f, 0.000000f, 0.000000f, 133.481105f, 0.000000f, 
	0.000000f, 0.000000f, 93.969410f, 0.000000f, 0.000000f, 133.481105f
};

static const tinytype Quu_inv_data[NINPUTS*NINPUTS]  = {
	0.426271f, 0.000000f, 0.000000f, 
	0.000000f, 0.426271f, 0.000000f, 
	0.000000f, 0.000000f, 0.426271f
};

static const tinytype AmBKt_data[NSTATES*NSTATES]  = {
	0.997293f, 0.000000f, 0.000000f, -0.108270f, 0.000000f, 0.000000f, 
	0.000000f, 0.997293f, 0.000000f, 0.000000f, -0.108270f, 0.000000f, 
	0.000000f, 0.000000f, 0.997293f, 0.000000f, 0.000000f, -0.108270f, 
	0.046246f, 0.000000f, 0.000000f, 0.849835f, 0.000000f, 0.000000f, 
	0.000000f, 0.046246f, 0.000000f, 0.000000f, 0.849835f, 0.000000f, 
	0.000000f, 0.000000f, 0.046246f, 0.000000f, 0.000000f, 0.849835f
};

static const tinytype APf_data[NSTATES]  = {0.000000f, 0.000000f, -42.485254f, 0.000000f, 0.000000f, -58.924682f};

static const tinytype BPf_data[NINPUTS]  = {0.000000f, 0.000000f, -3.393531f};

