/*
 * Author: Alejandro Valencia
 * Update: February 24, 2024
 */

#include "ccpd/cc_libraries/constants.h"
#include "pybind11/pybind11.h"
#include "pybind11/pytypes.h"

namespace py = pybind11;

namespace ccpd
{
namespace fluids
{

PYBIND11_MODULE(_constants, module)
{
    module.add_object("AIR_SPECIFIC_HEAT", py::float_(kAirSpecificHeat));
}

}  // namespace fluids

}  // namespace ccpd
