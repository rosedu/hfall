#ifndef __VERTEX__
#define __VERTEX__

#include "Vector3.h"
#include "Vector2.h"

namespace Engine
{
	class Vertex
	{
		public:
			Vertex();
			~Vertex();
		
		private:
			Vector3f position;
			Vector3f normal;
			Vector2f texel;
	};
}

#endif
