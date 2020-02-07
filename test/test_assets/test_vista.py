import pytest
from gempy.plot import vista as vs
import pyvista as pv
import os
import gempy as gp
from pickle import dump, load
input_path = os.path.dirname(__file__) + '/../../notebooks/data'


@pytest.fixture(scope="module")
def vista_obj() -> vs.Vista:
    """Return a GemPy Vista instance with basic geomodel attached."""
    geo_model = gp.create_data(
        [0, 2000, 0, 2000, 0, 2000], [50, 50, 50],
        path_o=input_path + '/input_data/tut_chapter1'
                            '/simple_fault_model_orientations.csv',
        path_i=input_path + '/input_data/tut_chapter1'
                            '/simple_fault_model_points.csv'
    )

    gp.set_series(
        geo_model,
        {"Fault_Series": 'Main_Fault',
         "Strat_Series": ('Sandstone_2', 'Siltstone', 'Shale', 'Sandstone_1')}
    )
    geo_model.set_is_fault(['Fault_Series'])

    with open("input_data/geomodel_sol.p", "rb") as f:
        geo_model.solutions = load(f)

    return vs.Vista(geo_model)


def test_set_bounds(vista_obj):
    vista_obj.set_bounds()


def test_plot_surface_points(vista_obj):
    mesh = vista_obj.plot_surface_points("Shale")
    assert vista_obj._actor_exists(mesh[0])


def test_plot_surface_points_all(vista_obj):
    meshes = vista_obj.plot_surface_points_all()
    for mesh in meshes:
        assert vista_obj._actor_exists(mesh)


def test_plot_orientations(vista_obj):
    meshes = vista_obj.plot_orientations("Shale")
    for mesh in meshes:
        assert vista_obj._actor_exists(mesh)


def test_plot_orientations_all(vista_obj):
    meshes = vista_obj.plot_orientations_all()
    for mesh in meshes:
        assert vista_obj._actor_exists(mesh)


def test_get_surface(vista_obj):
    surface = vista_obj.get_surface("Shale")
    assert type(surface) == pv.PolyData


def test_plot_surface(vista_obj):
    meshes = vista_obj.plot_surface("Shale")
    for mesh in meshes:
        assert vista_obj._actor_exists(mesh)


def test_plot_surfaces_all(vista_obj):
    meshes = vista_obj.plot_surfaces_all()
    for mesh in meshes:
        assert vista_obj._actor_exists(mesh)


def test_plot_structured_grid_lith(vista_obj):
    mesh = vista_obj.plot_structured_grid("lith")
    assert type(mesh[0]) == pv.StructuredGrid


# def test_plot_structured_grid_scalar(vista_obj):
#     mesh = vista_obj.plot_structured_grid("scalar")
#     assert type(mesh[0]) == pv.StructuredGrid


# def test_plot_structured_grid_values(vista_obj):
#     vista_obj.plot_structured_grid("values")
#     assert type(vista_obj._actors[0]) == pv.StructuredGrid





























