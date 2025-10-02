class BaseObj:
    def __init__(self, node_path, node_id):
        self.tag_lst = None
        self.node_path = node_path
        self.node_id = node_id

    # Получение значения в цикле
    def __getitem__(self, key):
        if key < len(self.tag_lst):
            return self.tag_lst[key]

    # Длина списка
    def loopCnt(self):
        return len(self.tag_lst)



class PID(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.CONFIG.SP_MIN', f'Application.{self.node_id}.sPID.SpMin'],
            [f'{self.node_path}.CONFIG.SP_MAX', f'Application.{self.node_id}.sPID.SpMax'],
            [f'{self.node_path}.CONFIG.EMIN', f'Application.{self.node_id}.sPID.ErrMin'],
            [f'{self.node_path}.CONFIG.EMAX', f'Application.{self.node_id}.sPID.ErrMax'],
            [f'{self.node_path}.CONFIG.TF', f'Application.{self.node_id}.sPID.Tf'],
            [f'{self.node_path}.CONFIG.UMIN', f'Application.{self.node_id}.sPID.MvMin'],
            [f'{self.node_path}.CONFIG.UMAX', f'Application.{self.node_id}.sPID.MvMax'],
            [f'{self.node_path}.CONFIG.PV_MIN', f'Application.{self.node_id}.sPID.PvMin'],
            [f'{self.node_path}.CONFIG.PV_MAX', f'Application.{self.node_id}.sPID.PvMax'],
            [f'{self.node_path}.K', f'Application.{self.node_id}.sPID.K'],
            [f'{self.node_path}.Ti', f'Application.{self.node_id}.sPID.Ti'],
            [f'{self.node_path}.Td', f'Application.{self.node_id}.sPID.Td'],
            [f'{self.node_path}.AUTO_SP_ON', f'Application.{self.node_id}.sPID.SpMode'],
            [f'{self.node_path}.SP', f'Application.{self.node_id}.sPID.SpLoc'],
            [f'{self.node_path}.MAN_ON', f'Application.{self.node_id}.sPID.ManMode'],
            [f'{self.node_path}.MAN_U', f'Application.{self.node_id}.sPID.MvMan'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sPID.Diagn'],
            [f'{self.node_path}.U', f'Application.{self.node_id}.sPID.Mv'],
            [f'{self.node_path}.SP_ON', f'Application.{self.node_id}.sPID.SpOn'],
            [f'{self.node_path}.SP_FACT', f'Application.{self.node_id}.sPID.SpFact'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sPID.Mode'],
            [f'{self.node_path}.SP_OUT.VALUE', f'Application.{self.node_id}.sPID.SpOut.VALUE'],
            [f'{self.node_path}.SP_OUT.QUALITY', f'Application.{self.node_id}.sPID.SpOut.QUALITY'],
            [f'{self.node_path}.E.VALUE', f'Application.{self.node_id}.sPID.Err.VALUE'],
            [f'{self.node_path}.E.QUALITY', f'Application.{self.node_id}.Err.QUALITY'],
            [f'{self.node_path}.PV.VALUE', f'Application.{self.node_id}..sPID.Pv.VALUE'],
            [f'{self.node_path}.PV.QUALITY', f'Application.{self.node_id}.sPID.Pv.QUALITY'],
            [f'{self.node_path}.BALANCE', f'Application.{self.node_id}.sPID.Balance'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sPID.MsgOff']
        ]


class MTR(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.HMI_CMD', f'Application.{self.node_id}.sMtr.HmiCmd'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sMtr.Diagn'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sMtr.Mode'],
            [f'{self.node_path}.RQST_W', f'Application.{self.node_id}.sMtr.RqstW'],
            [f'{self.node_path}.CTL_W', f'Application.{self.node_id}.sMtr.CtlW'],
            [f'{self.node_path}.HMI_BLOCK', f'Application.{self.node_id}.sMtr.HmiBlock'],
            [f'{self.node_path}.BLOCK', f'Application.{self.node_id}.sMtr.Block'],
            [f'{self.node_path}.STATE', f'Application.{self.node_id}.sMtr.State'],
            [f'{self.node_path}.WORKTIME', f'Application.{self.node_id}.sMtr.Worktime'],
            [f'{self.node_path}.CURRENT.VALUE', f'Application.{self.node_id}.sMtr.sCurrent.VALUE'],
            [f'{self.node_path}.CURRENT.QUALITY', f'Application.{self.node_id}.sMtr.sCurrent.QUALITY'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sMtr.Imit'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sMtr.MsgOff'],
            [f'{self.node_path}.SET_MODE', f'Application.{self.node_id}.sMtr.SetMode'],
            [f'{self.node_path}.FREQ.VALUE', f'Application.{self.node_id}.sMtr.sFreq.VALUE'],
            [f'{self.node_path}.FREQ.QUALITY', f'Application.{self.node_id}.sMtr.sFreq.QUALITY'],
            [f'{self.node_path}.BLOCK_OFF', f'Application.{self.node_id}.sMtr.InterlockSet'],
            [f'{self.node_path}.SP_FREQ', f'Application.{self.node_id}.sFC.SpFreq'],
            [f'{self.node_path}.MAX_CURRENT', f'Application.{self.node_id}.sMtr.MaxCurrent'],
            [f'{self.node_path}.CNT_ON', f'Application.{self.node_id}.sMtr.CntOn'],
            [f'{self.node_path}.CHECKLIST', f'Application.{self.node_id}.sMtr.CheckList']
        ]


class VLVD(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.CONFIG.OPN_TIME', f'Application.{self.node_id}.sVlv.OpnTime'],
            [f'{self.node_path}.CONFIG.CLS_TIME', f'Application.{self.node_id}.sVlv.ClsTime'],
            [f'{self.node_path}.SET_MODE', f'Application.{self.node_id}.sVlv.SetMode'],
            [f'{self.node_path}.HMI_CMD', f'Application.{self.node_id}.sVlv.HmiCmd'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sVlv.Diagn'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sVlv.Mode'],
            [f'{self.node_path}.RQST_W', f'Application.{self.node_id}.sVlv.RqstW'],
            [f'{self.node_path}.CTL_W', f'Application.{self.node_id}.sVlv.CtlW'],
            [f'{self.node_path}.HMI_BLOCK', f'Application.{self.node_id}.sVlv.HmiBlock'],
            [f'{self.node_path}.BLOCK', f'Application.{self.node_id}.sVlv.Block'],
            [f'{self.node_path}.STATE', f'Application.{self.node_id}.sVlv.State'],
            [f'{self.node_path}.TIMEOUT', f'Application.{self.node_id}.sVlv.TimeOut'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sVlv.Imit'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sVlv.MsgOff'],
            [f'{self.node_path}.BLOCK_OFF', f'Application.{self.node_id}.sVlv.BLOCK_OFF']
        ]


class VLVA(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.CONFIG.RUNTIME', f'Application.{self.node_id}.sVlv.sConfig.RUNTIME'],
            [f'{self.node_path}.CONFIG.PERC_OPN', f'Application.{self.node_id}.sVlv.PercOpn'],
            [f'{self.node_path}.CONFIG.PERC_CLS', f'Application.{self.node_id}.sVlv.PercCls'],
            [f'{self.node_path}.CONFIG.DELAYERR', f'Application.{self.node_id}.sVlv.DelayErr'],
            [f'{self.node_path}.CONFIG.DELTA', f'Application.{self.node_id}.sVlv.Delta'],
            [f'{self.node_path}.SP', f'Application.{self.node_id}.sVlv.MvMan'],
            [f'{self.node_path}.SET_MODE', f'Application.{self.node_id}.sVlv.SetMode'],
            [f'{self.node_path}.HMI_CMD', f'Application.{self.node_id}.sVlv.HmiCmd'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sVlv.Diagn'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sVlv.Mode'],
            [f'{self.node_path}.RQST_W', f'Application.{self.node_id}.sVlv.RqstW'],
            [f'{self.node_path}.HMI_BLOCK', f'Application.{self.node_id}.sVlv.HmiBlock'],
            [f'{self.node_path}.BLOCK', f'Application.{self.node_id}.sVlv.Block'],
            [f'{self.node_path}.STATE', f'Application.{self.node_id}.sVlv.State'],
            [f'{self.node_path}.U', f'Application.{self.node_id}.sVlv.Mv'],
            [f'{self.node_path}.INH', f'Application.{self.node_id}.sVlv.Inh'],
            [f'{self.node_path}.PI.VALUE', f'Application.{self.node_id}.sVlv.Pos.VALUE'],
            [f'{self.node_path}.PI.QUALITY', f'Application.{self.node_id}.sVlv.Pos.STATUS'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sVlv.Imit'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sVlv.MsgOff'],
            [f'{self.node_path}.BLOCK_OFF', f'Application.{self.node_id}.sVlv.InterlockSet']
        ]


class DI(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        # Вложенный список с Node_path и node_id для создания объектов XML
        # 0 - путь к объекту по вложенным папкам в AStudio (SinLib.di.MSG_OFF)
        # 1 - путь тегу в OPCUA ПЛК (Application.DI_DI1.sDI.MsgOff)
        self.tag_lst = [
            [f'{self.node_path}.INV_ON', f'Application.{self.node_id}.sDI.Inv'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sDI.Mode'],
            [f'{self.node_path}.IMIT_VALUE', f'Application.{self.node_id}.sDI.ImitValue'],
            [f'{self.node_path}.OUT.VALUE', f'Application.{self.node_id}.sDI.Out.VALUE'],
            [f'{self.node_path}.OUT.QUALITY', f'Application.{self.node_id}.sDI.Out.QUALITY'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sDI.Diagn'],
            [f'{self.node_path}.FLT_EN', f'Application.{self.node_id}.sDI.EnFlt'],
            [f'{self.node_path}.FLT_TM', f'Application.{self.node_id}.sDI.FltrTime'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sDI.MsgOff'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sDI.Imit'],
            [f'{self.node_path}.RAW', f'Application.{self.node_id}.sDI.RAW']
        ]


class AI(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.CONFIG.YMIN', f'Application.{self.node_id}.sAI.Ymin'],
            [f'{self.node_path}.CONFIG.YMAX', f'Application.{self.node_id}.sAI.Ymax'],
            [f'{self.node_path}.CONFIG.AH', f'Application.{self.node_id}.sAI.Ah'],
            [f'{self.node_path}.CONFIG.WH', f'Application.{self.node_id}.sAI.Wh'],
            [f'{self.node_path}.CONFIG.WL', f'Application.{self.node_id}.sAI.Wl'],
            [f'{self.node_path}.CONFIG.AL', f'Application.{self.node_id}.sAI.Al'],
            [f'{self.node_path}.CONFIG.TF', f'Application.{self.node_id}.sAI.Tf'],
            [f'{self.node_path}.CONFIG.HYST', f'Application.{self.node_id}.sAI.Hyst'],
            [f'{self.node_path}.CONFIG.SIGN_CHECK', f'Application.{self.node_id}.sAI.SignCheck'],
            [f'{self.node_path}.CONFIG.AH2', f'Application.{self.node_id}.sAI.Ah2'],
            [f'{self.node_path}.CONFIG.AL2', f'Application.{self.node_id}.sAI.Al2'],
            [f'{self.node_path}.CONFIG.TH', f'Application.{self.node_id}.sAI.Th'],
            [f'{self.node_path}.CONFIG.TL', f'Application.{self.node_id}.sAI.Tl'],
            [f'{self.node_path}.CONFIG.TM_AH2', f'Application.{self.node_id}.sAI.TmAh2'],
            [f'{self.node_path}.CONFIG.TM_AH', f'Application.{self.node_id}.sAI.TmAh'],
            [f'{self.node_path}.CONFIG.TM_WH', f'Application.{self.node_id}.sAI.TmWh'],
            [f'{self.node_path}.CONFIG.TM_TH', f'Application.{self.node_id}.sAI.TmTh'],
            [f'{self.node_path}.CONFIG.TM_TL', f'Application.{self.node_id}.sAI.TmTl'],
            [f'{self.node_path}.CONFIG.TM_WL', f'Application.{self.node_id}.sAI.TmWl'],
            [f'{self.node_path}.CONFIG.TM_AL', f'Application.{self.node_id}.sAI.TmAl'],
            [f'{self.node_path}.CONFIG.TM_AL2', f'Application.{self.node_id}.sAI.TmAl2'],
            [f'{self.node_path}.OUT.VALUE', f'Application.{self.node_id}.sAI.Out.VALUE'],
            [f'{self.node_path}.OUT.QUALITY', f'Application.{self.node_id}.Out.QUALITY'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sAI.Imit'],
            [f'{self.node_path}.IMIT_VALUE', f'Application.{self.node_id}.sAI.ImitValue'],
            [f'{self.node_path}.FACT_VALUE', f'Application.{self.node_id}.sAI.FactValue'],
            [f'{self.node_path}.SIGN', f'Application.{self.node_id}.sAI.Sign'],
            [f'{self.node_path}.MODE', f'Application.{self.node_id}.sAI.Mode'],
            [f'{self.node_path}.DIAGN', f'Application.{self.node_id}.sAI.Diagn'],
            [f'{self.node_path}.MSG_OFF', f'Application.{self.node_id}.sAI.MsgOffl'],
            [f'{self.node_path}.LMT_CHECK', f'Application.{self.node_id}.sAI.LimitCheck'],
            [f'{self.node_path}.RAW', f'Application.{self.node_id}.sAI.Raw'],
            [f'{self.node_path}.BAD_TYPE', f'Application.{self.node_id}.sAI.BadType'],
            [f'{self.node_path}.BAD_VALUE', f'Application.{self.node_id}.sAI.BadValue']
        ]


class FC_CTRL(BaseObj):
    def __init__(self, node_path, node_id):
        super().__init__(node_path, node_id)
        self.tag_lst = [
            [f'{self.node_path}.HMI_CMD', f'Application.{self.node_id}.sFC.HmiCmd'],
            [f'{self.node_path}.STATE', f'Application.{self.node_id}.sFC.State'],
            [f'{self.node_path}.IMIT', f'Application.{self.node_id}.sFC.Imit'],
            [f'{self.node_path}.SP_FREQ', f'Application.{self.node_id}.sFC.SpFreq'],
            [f'{self.node_path}.FREQ', f'Application.{self.node_id}.sFC.PvFreq'],
            [f'{self.node_path}.CURRENT', f'Application.{self.node_id}.sFC.fcPvCurr'],
            [f'{self.node_path}.ERR_CODE', f'Application.{self.node_id}.sFC.ErrCode']
        ]
