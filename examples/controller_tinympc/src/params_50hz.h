static sfloat Kinf_data[NINPUTS*NSTATES] = {
  -0.089412f,0.086423f,0.067816f,-0.064828f,
  0.084394f,0.072629f,-0.075797f,-0.081226f,
  0.561104f,0.561104f,0.561104f,0.561104f,
  -0.475665f,-0.359315f,0.380735f,0.454245f,
  -0.542625f,0.521945f,0.304785f,-0.284105f,
  -0.708036f,0.729571f,-0.780548f,0.759012f,
  -0.077112f,0.074341f,0.053401f,-0.050631f,
  0.070987f,0.058631f,-0.061537f,-0.068082f,
  0.247898f,0.247898f,0.247898f,0.247898f,
  -0.043822f,-0.026304f,0.028353f,0.041773f,
  -0.055214f,0.053217f,0.016502f,-0.014505f,
  -0.301843f,0.307663f,-0.321421f,0.315601f,
};
static sfloat Pinf_data[NSTATES*NSTATES] = {
  1843.205101f,-5.315172f,0.000000f,28.686652f,1927.507176f,215.625883f,590.159039f,-4.510432f,-0.000000f,2.080558f,19.154654f,63.388445f,
  -5.315172f,1834.759303f,0.000000f,-1881.094421f,-28.735278f,-85.878969f,-4.513652f,582.902158f,-0.000000f,-15.855003f,-2.086260f,-25.252849f,
  0.000000f,0.000000f,13806.362214f,-0.000000f,0.000000f,-0.000000f,0.000000f,0.000000f,2755.536630f,-0.000000f,-0.000000f,-0.000000f,
  28.686652f,-1881.094421f,-0.000000f,9194.053682f,207.344898f,840.193717f,27.081076f,-1501.986628f,-0.000000f,84.807597f,20.176150f,276.693688f,
  1927.507176f,-28.735278f,0.000000f,207.344898f,9556.059350f,2105.056988f,1547.400172f,-27.104305f,0.000000f,20.166353f,121.302917f,692.994014f,
  215.625883f,-85.878969f,-0.000000f,840.193717f,2105.056988f,46431.066857f,228.175885f,-90.971593f,-0.000000f,107.588424f,269.317811f,4475.218984f,
  590.159039f,-4.513652f,-0.000000f,27.081076f,1547.400172f,228.175885f,390.094849f,-3.984785f,-0.000000f,2.159882f,16.711997f,69.372979f,
  -4.510432f,582.902158f,-0.000000f,-1501.986628f,-27.104305f,-90.971593f,-3.984785f,383.547711f,-0.000000f,-13.069708f,-2.163254f,-27.666736f,
  0.000000f,0.000000f,2755.536630f,-0.000000f,0.000000f,-0.000000f,0.000000f,0.000000f,1192.975645f,-0.000000f,-0.000000f,-0.000000f,
  2.080558f,-15.855003f,0.000000f,84.807597f,20.166353f,107.588424f,2.159882f,-13.069708f,-0.000000f,10.543047f,3.032728f,44.820946f,
  19.154654f,-2.086260f,-0.000000f,20.176150f,121.302917f,269.317811f,16.711997f,-2.163254f,-0.000000f,3.032728f,16.409852f,112.146852f,
  63.388445f,-25.252849f,-0.000000f,276.693688f,692.994014f,4475.218984f,69.372979f,-27.666736f,-0.000000f,44.820946f,112.146852f,1901.295015f,
};
static sfloat Quu_inv_data[NINPUTS*NINPUTS] = {
  0.001295f,0.000003f,0.000721f,-0.000004f,
  0.000003f,0.001270f,-0.000001f,0.000743f,
  0.000721f,-0.000001f,0.001285f,0.000010f,
  -0.000004f,0.000743f,0.000010f,0.001265f,
};
static sfloat AmBKt_data[NSTATES*NSTATES] = {
  0.999994f,-0.000000f,-0.000000f,0.000001f,0.004201f,0.000002f,0.019995f,-0.000000f,-0.000000f,0.000000f,0.000011f,0.000001f,
  -0.000000f,0.999994f,0.000000f,-0.004201f,-0.000001f,-0.000001f,-0.000000f,0.019995f,0.000000f,-0.000011f,-0.000000f,-0.000000f,
  -0.000000f,-0.000000f,0.997840f,0.000000f,-0.000000f,0.000000f,-0.000000f,-0.000000f,0.019046f,0.000000f,-0.000000f,-0.000000f,
  0.000248f,0.008904f,-0.000000f,0.952668f,0.001070f,0.001129f,0.000189f,0.007349f,-0.000000f,0.006026f,0.000076f,0.000312f,
  -0.008794f,-0.000245f,0.000000f,0.001044f,0.952887f,0.002977f,-0.007282f,-0.000186f,-0.000000f,0.000074f,0.006029f,0.000822f,
  0.000517f,-0.000197f,0.000000f,0.001024f,0.002681f,0.998616f,0.000424f,-0.000162f,0.000000f,0.000081f,0.000212f,0.009451f,
  -0.000968f,-0.000027f,-0.000000f,0.000115f,0.387212f,0.000328f,0.999198f,-0.000020f,-0.000000f,0.000008f,0.001370f,0.000091f,
  -0.000027f,-0.000980f,0.000000f,-0.387188f,-0.000118f,-0.000124f,-0.000021f,0.999191f,0.000000f,-0.001369f,-0.000008f,-0.000034f,
  -0.000000f,0.000000f,-0.215994f,0.000000f,-0.000000f,0.000000f,-0.000000f,-0.000000f,0.904573f,0.000000f,-0.000000f,-0.000000f,
  0.049642f,1.780747f,-0.000000f,-9.466462f,0.213900f,0.225885f,0.037793f,1.469791f,-0.000000f,0.205141f,0.015270f,0.062393f,
  -1.758793f,-0.048929f,-0.000000f,0.208759f,-9.422625f,0.595481f,-1.456389f,-0.037112f,-0.000000f,0.014811f,0.205834f,0.164456f,
  0.103424f,-0.039398f,0.000000f,0.204832f,0.536111f,-0.276818f,0.084804f,-0.032348f,0.000000f,0.016184f,0.042310f,0.890102f,
};
static sfloat coeff_d2p_data[NSTATES*NINPUTS] = {
  -0.000001f,0.000001f,-0.000001f,0.000021f,0.000027f,0.000062f,0.000003f,-0.000002f,-0.000000f,0.000000f,0.000001f,0.000010f,
  0.000001f,0.000001f,-0.000001f,0.000014f,-0.000024f,-0.000063f,-0.000002f,-0.000001f,-0.000000f,-0.000000f,-0.000001f,-0.000010f,
  0.000000f,-0.000001f,-0.000001f,-0.000018f,-0.000020f,0.000065f,-0.000002f,0.000002f,-0.000000f,0.000000f,0.000000f,0.000010f,
  -0.000000f,-0.000001f,-0.000001f,-0.000017f,0.000017f,-0.000065f,0.000002f,0.000002f,-0.000000f,-0.000000f,-0.000000f,-0.000010f,
};
static sfloat Q_data[NSTATES*NSTATES] = {
  44.444444f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,44.444444f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,625.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,4.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,4.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,1111.111111f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,6.250000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,6.250000f,0.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,6.250000f,0.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,6.250000f,0.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,6.250000f,0.000000f,
  0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,0.000000f,100.000000f,
};
static sfloat R_data[NINPUTS*NINPUTS] = {
  400.000000f,0.000000f,0.000000f,0.000000f,
  0.000000f,400.000000f,0.000000f,0.000000f,
  0.000000f,0.000000f,400.000000f,0.000000f,
  0.000000f,0.000000f,0.000000f,400.000000f,
};
