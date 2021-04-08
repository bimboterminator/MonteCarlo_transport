import vtk
def mkVtkIdList(it):
    """
    Makes a vtkIdList from a Python iterable. I'm kinda surprised that
     this is necessary, since I assumed that this kind of thing would
     have been built into the wrapper and happen transparently, but it
     seems not.

    :param it: A python iterable.
    :return: A vtkIdList
    """
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil


def main(tracks,thick):
    #colors = vtk.vtkNamedColors()

    thickness = thick
    plate = [(-50,5,-50), (-50,5,50), (50,5,50), (50,5,-50),(-50,5+thickness,-50),(-50,5+thickness,50),(50,5+thickness,50),(50,5+thickness,-50)]


    # pts = array of 6 4-tuples of vtkIdType (int) representing the faces
    #     of the cube in terms of the above vertices
    pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

    cube = vtk.vtkPolyData()
    cube_points = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    #scalars = vtk.vtkFloatArray()

    for i, xi in enumerate(plate):
        cube_points.InsertPoint(i, xi)
    for pt in pts:
        polys.InsertNextCell(mkVtkIdList(pt))

    cube.SetPoints(cube_points)
    cube.SetPolys(polys)

    cubeMapper = vtk.vtkPolyDataMapper()
    cubeMapper.SetInputData(cube)
    cubeActor = vtk.vtkActor()
    cubeActor.SetMapper(cubeMapper)

    cubeActor.GetProperty().SetOpacity(0.4)

    ren1 = vtk.vtkRenderer()


    for t in range(len(tracks)):
        polygon = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()
    #scalars = vtk.vtkFloatArray()

    # Load the point, cell, and data attributes.
        for i, xi in enumerate(tracks[t]):
            points.InsertPoint(i, xi)

        lines.InsertNextCell(len(tracks[t]))
        for i in range(len(tracks[t])):
            lines.InsertCellPoint(i)


    # We now assign the pieces to the vtkPolyData.
        polygon.SetPoints(points)
        polygon.SetLines(lines)
   # cube.GetPointData().SetScalars(scalars)

    # Now we'll look at it.
        polygonMapper = vtk.vtkPolyDataMapper()
        polygonMapper.SetInputData(polygon)
        polygonMapper.Update()
        polygonActor = vtk.vtkActor()
        polygonActor.SetMapper(polygonMapper)
        ren1.AddActor(polygonActor)
    # The usual rendering stuff.


    ren1.AddActor(cubeActor)
    #ren1.SetBackground(0.1, 0.2, 0.4)

    # Automatically set up the camera based on the visible actors.
    # The camera will reposition itself to view the center point of the actors,
    # and move along its initial view plane normal
    # (i.e., vector defined from camera position to focal point) so that all of the
    # actors can be seen.
    ren1.ResetCamera()

    # Finally we create the render window which will show up on the screen
    # We put our renderer into the render window using AddRenderer. We
    # also set the size to be 300 pixels by 300.
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(300, 300)

    # The vtkRenderWindowInteractor class watches for events (e.g., keypress,
    # mouse) in the vtkRenderWindow. These events are translated into
    # event invocations that VTK understands (see VTK/Common/vtkCommand.h
    # for all events that VTK processes). Then observers of these VTK
    # events can process them as appropriate.
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()
    iren.Start()


