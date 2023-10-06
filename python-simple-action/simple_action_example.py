import io
import re
from contextlib import redirect_stdout

from mlp_sdk.abstract import Task
from mlp_sdk.hosting.host import host_mlp_cloud
from mlp_sdk.transport.MlpServiceSDK import MlpServiceSDK
from pydantic import BaseModel
from typing import List
from rayoptics.environment import *
from rayoptics.util.misc_math import normalize

def calc_loss(opm):
    efl_for_loss=5                      #mm
    fD_for_loss=2.1
    total_length_for_loss=7.0             #mm
    radius_enclosed_energy_for_loss=50    #micron
    perc_max_enclosed_energy_for_loss=80    #%
    perc_min_enclosed_energy_for_loss=50    #%
    min_thickness_for_loss=0.1              #mm
    min_thickness_air_for_loss=0.0            #mm
    number_of_field=3 #5
    number_of_wavelength=2

    def funct_loss_enclosed_energy(enclosed_energy,perc_max_enclosed_energy_for_loss,perc_min_enclosed_energy_for_loss):
        if enclosed_energy<perc_max_enclosed_energy_for_loss:
            if enclosed_energy<perc_min_enclosed_energy_for_loss:
                loss_enclosed_energy=1e3
            else:
                loss_enclosed_energy=(perc_max_enclosed_energy_for_loss-enclosed_energy)
        else:
            loss_enclosed_energy=0
        return loss_enclosed_energy

    def get_thichness(sm):
        f = io.StringIO()
        with redirect_stdout(f):
            sm.list_model()
        s = f.getvalue()
        rows = re.split(r"\n", s)
        thickness_list = []
        thickness_material_list=[]
        thickness_air_list=[]
        for row in rows[1:-1]:
            row = re.sub(r'\s+',r'!', row)
            values = re.split(r"!", row)
            if values[4]!='air' and values[4]!='1':
                thickness_material_list.append(float(values[3]))
            if values[4]=='air' and values[4]!='1':
                thickness_air_list.append(float(values[3]))
            thickness_list.append(float(values[3]))      #3 - thickness, 2 - curvature, 4 - type of material
        number_of_surfaces=len(rows)-2
        return thickness_list, thickness_material_list, thickness_air_list, number_of_surfaces

    # opm = open_model(f'{path2model}', info=True)

    sm = opm['seq_model']
    osp = opm['optical_spec']
    pm = opm['parax_model']
    em = opm['ele_model']
    pt = opm['part_tree']
    ar = opm['analysis_results']

    pm.__dict__

    efl=pm.opt_model['analysis_results']['parax_data'].fod.efl
    fD=pm.opt_model['analysis_results']['parax_data'].fod.fno


    ax_ray, pr_ray, fod = ar['parax_data']
    u_last = ax_ray[-1][mc.slp]
    central_wv = opm.nm_to_sys_units(sm.central_wavelength())
    n_last = pm.sys[-1][mc.indx]
    to_df = compute_third_order(opm)

    tr_df=to_df.apply(to.seidel_to_transverse_aberration, axis='columns', args=(n_last,u_last))
    distortion=tr_df.to_numpy()[-1,5]

    field=0
    psf = SpotDiagramFigure(opm)
    test_psf = psf.axis_data_array[field][0][0][0]
    test_psf[:,1]=test_psf[:,1]-np.mean(test_psf[:,1])
    plt.plot(test_psf[:,0],test_psf[:,1],'o')
    plt.rcParams['figure.figsize'] = (8, 8)



    fld, wvl, foc = osp.lookup_fld_wvl_focus(0)
    sm.list_model()
    sm.list_surfaces()
    efl=pm.opt_model['analysis_results']['parax_data'].fod.efl

    pm.first_order_data()
    opm.update_model()

    # total_length=0
    # min_thickness=0.15
    if abs(efl-efl_for_loss)>0.25:
        loss_focus=1e2*(efl-efl_for_loss)**2
    else:
        loss_focus=0

    if abs(fD)>=fD_for_loss:
        loss_FD=5*1e4*(fD-fD_for_loss)**2
    else:
        loss_FD=0


    thickness_list,thickness_material_list,thickness_air_list, number_of_surfaces=get_thichness(sm)
    total_length=np.sum(thickness_list[1:])
    min_thickness=np.min(thickness_material_list)
    min_thickness_air=np.min(thickness_air_list)
    if (total_length-total_length_for_loss)>0:
        loss_total_length=1e4*(total_length-total_length_for_loss)**2
    else:
        loss_total_length=0

    if min_thickness<min_thickness_for_loss:
        loss_min_thickness=1e6*(min_thickness-min_thickness_for_loss)**2
    else:
        loss_min_thickness=0

    if min_thickness_air<min_thickness_air_for_loss:
        loss_min_thickness_air=8e4*(min_thickness_air-min_thickness_air_for_loss)**2
    else:
        loss_min_thickness_air=0


    loss_enclosed_energy_all=0
    loss_rms_all=0
    temp=0
    for idx_field in range(number_of_field):
        for idx_wavelength in range(number_of_wavelength):
            test_psf = psf.axis_data_array[idx_field][0][0][idx_wavelength]
            test_psf[:,1]=test_psf[:,1]-np.mean(test_psf[:,1])
            r_psf=np.sort(np.sqrt(test_psf[:,0]**2+test_psf[:,1]**2))
            enclosed_energy=100*np.sum(r_psf<=radius_enclosed_energy_for_loss/1e3)/len(test_psf[:,0])
            loss_enclosed_energy=funct_loss_enclosed_energy(enclosed_energy,perc_max_enclosed_energy_for_loss,perc_min_enclosed_energy_for_loss)
            loss_enclosed_energy_all=loss_enclosed_energy_all+loss_enclosed_energy

            dl=int(np.floor(len(test_psf[:,0])*perc_max_enclosed_energy_for_loss/100))
            loss_rms=np.sqrt(np.sum((1e3*r_psf[:dl])**2)/dl)
            loss_rms_all=loss_rms_all+loss_rms

            temp=temp+1
    loss_enclosed_energy_all=loss_enclosed_energy_all/temp
    loss_rms_all=loss_rms_all/temp
    loss=loss_focus+loss_FD+loss_total_length+loss_min_thickness+loss_min_thickness_air+loss_enclosed_energy_all+loss_rms_all
    # layout_plt0 = plt.figure(FigureClass=InteractiveLayout, opt_model=opm,
    #                         do_draw_rays=True, do_paraxial_layout=False,
    #                         is_dark=isdark).plot()
    return(loss)

def calc_loss_by_point(point):
    isdark = False  # Не трогаем

    opm = OpticalModel()  # create new model
    # opm = open_model('test.roa') # load model from file

    sm = opm['seq_model']
    osp = opm['optical_spec']
    pm = opm['parax_model']
    em = opm['ele_model']
    pt = opm['part_tree']
    ar = opm['analysis_results']

    opm.system_spec.title = 'Test_epoch_1'  # Поидеи это поле нам не нужно
    opm.system_spec.dimensions = 'mm'  # Не трогаем

    # pupil - размер входного зрачка (диафрагмы)
    # osp['pupil'] = PupilSpec(osp, key=['image', 'f/#'], value=2.5)
    osp['fov'] = FieldSpec(osp, key=['image', 'height'], value=3.5, is_relative=True,
                           flds=[0., 0.05, 0.1, 0.15, 0.2, 0.9])
    osp['wvls'] = WvlSpec([('F', 0.5), ('d', 1.0), ('C', 0.5), ], ref_wl=1)

    sm.do_apertures = True
    sm.gaps[0].thi = 1e10

    # [curvature, t, 1.('medium' до заяптой), medium (после запятой без нуля на конце)], sd это surface_od,
    # 1 surface - lens
    curvature_1 = 0.2747823174694503
    t_1 = 1
    medium_1_1 = 1.540
    medium_2_1 = 75.0
    sd_1 = 1.3159821701196845
    r_1 = 3.639244363353831
    coefs_1 = [0.0, 0.009109298409282469, -0.03374649200850791, 0.01797256809388843, -0.0050513483804677005, 0.0,
               0.0, 0.0]

    sm.add_surface([curvature_1, t_1, medium_1_1, medium_2_1], sd=sd_1)
    sm.ifcs[sm.cur_surface].profile = EvenPolynomial(r=r_1, coefs=coefs_1)
    sm.ifcs[sm.cur_surface].profile.sd = sd_1

    sm.set_stop()

    # 4 surface - air
    curvature_4 = -0.2568888474926888
    t_4 = 4.216392884493065
    sd_4 = 1.608772352457493

    sm.add_surface([curvature_4, t_4], sd=sd_4)
    sm.ifcs[sm.cur_surface].profile.sd = sd_4

    opm.update_model()

    sm.do_apertures = False
    return calc_loss(opm)
class PredictRequest(BaseModel):

    points: List[List[float]]
    def __int__(self, points):
        self.points = points



class PredictResponse(BaseModel):
    loss: List[float]

    def __int__(self, loss):
        self.loss = loss


class SimpleActionExample(Task):

    def __init__(self, config: BaseModel, service_sdk: MlpServiceSDK = None) -> None:
        super().__init__(config, service_sdk)


    def predict(self, data: PredictRequest, config: BaseModel) -> PredictResponse:
        loss = []
        for point in data.points:
            loss.append(calc_loss_by_point(point))
        return PredictResponse(loss = loss)



if __name__ == "__main__":
    host_mlp_cloud(SimpleActionExample, BaseModel())
