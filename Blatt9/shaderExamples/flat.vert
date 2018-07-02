// Gouraud vertex shader from 
// Richard S. Wright Jr. 
// OpenGL SuperBible
//#version 330

uniform vec4 ambientColor; 
uniform vec4 diffuseColor; 
uniform vec4 specularColor; 

uniform vec3 vLightPosition; 

uniform mat4 mvpMatrix; 
uniform mat4 mvMatrix; 
uniform mat3 normalMatrix; 

varying vec4 vVaryingColor;

void main(void)
{
    // Get surface normal in eye coordinates
    vec3 vEyeNormal = normalize(normalMatrix * gl_Normal); 

    // Get vertex position in eye coordinates
    vec4 vPosition4 = mvMatrix * gl_Vertex; 
    vec3 vPosition3 = vPosition4.xyz / vPosition4.w;
    
    // Get vector to light source
    vec3 vLightDir = normalize(vLightPosition - vPosition3);
    
	// Dot product gives the diffuse intensity
	float diff = max(0.0, dot(vEyeNormal, vLightDir)); 
	
	// Multiply intensity by diffuse color, force alpha to 1.0
	vVaryingColor = diff * diffuseColor; 

	// Add in ambient light
	vVaryingColor += ambientColor;
	
	// Specular light
	vec3 vReflection = normalize(reflect(-vLightDir, vEyeNormal));
	float spec = max(0.0, dot(vEyeNormal, vReflection));
	if (diff != 0.0) {
		float fSpec = pow(spec, 128.0);
		vVaryingColor.rgb += vec3(fSpec, fSpec, fSpec);
	}
	
    // Transform the geometry
    gl_Position = mvpMatrix * gl_Vertex; 
}