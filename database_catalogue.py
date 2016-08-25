import pickle
import os
import sys

import numpy as np
from datetime import datetime
from darten_gui import Darters, Leg, Set, Match
import matplotlib.pyplot as plt

if sys.version[0] == str(2):
    import Tkinter as tkinter
    import ttk
else:
    import tkinter
    from tkinter import ttk


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class overview:

    def __init__(self):

        self.__mainWindow = tkinter.Tk()

        self.mainframes = {}
        self.listboxes = {}
        self.labels = AutoVivification()
        self.player_labels = AutoVivification()
        self.buttons = {}
        self.optionmenus = AutoVivification()

        self.players = data_load['player_list']
        self.selected_player = self.players[0]
        self.getting_playerstats(self.selected_player, data_load)

        """ Frames """
        self.define_main_frames_dict()
        for name, frame in self.MainFrames.items():
            self.mainframes[name] = self.create_frame(**frame)

#        self.define_sub_frames_dict()
#        for name, frame in self.SubFrames.items():
#            self.subframes[name] = self.create_frame(**frame)

        """ Listboxes """
        self.define_listboxes_dict()
        for name, listbox in self.Listboxes.items():
            self.listboxes[name] = self.create_listbox(**listbox)

        """ Menus """
        self.define_optionmenus_dict()
        for optionmenu in self.Optionmenus.values():
            self.optionmenus[optionmenu['name']]['menu'], \
                self.optionmenus[optionmenu['name']]['variable'] = \
                self.create_optionmenu(**optionmenu)

        """ Buttons """
        self.define_buttons_dict()
        for name, button in self.Buttons.items():
            self.buttons[name] = self.create_button(**button)

        """ Labels """
        self.define_labels_dict()
        for name, label in self.Labels.items():
            self.labels[name]['label'] = self.create_labels(self.labels,
                                                            name=name, **label)

        """ Initialize stats in listbox and match stats """
        self.filling_listbox(self.listboxes['match_box'])
        self.listboxes['match_box'].selection_clear(0, tkinter.END)
        self.listboxes['match_box'].selection_set(0)
        self.print_match_stats(self.listboxes['match_box'])

        tkinter.mainloop()

    def define_main_frames_dict(self):
        self.MainFrames = {}
        self.add_to_frame_dict(self.MainFrames, 'top_frame',
                               self.__mainWindow, row=1, col=1)
        self.add_to_frame_dict(self.MainFrames, 'match_overview',
                               self.__mainWindow, row=2, col=1)
        self.add_to_frame_dict(self.MainFrames, 'player_overview',
                               self.__mainWindow, row=1, col=2)
        self.add_to_frame_dict(self.MainFrames, 'graph_frame',
                               self.__mainWindow, row=2, col=2, rowspan=1)

    def define_buttons_dict(self):
        self.Buttons = {}
        self.add_to_button_dict(self.Buttons, 'savehistogram',
                                self.mainframes['top_frame'],
                                text='Save histogram', row=1, col=2,
                                bindings={'<Return>': self.savefigure,
                                          '<Button-1>': self.savefigure},
                                width=10)

    def define_listboxes_dict(self):
        self.Listboxes = {}
        self.add_to_listbox_dict(self.Listboxes, 'match_box',
                                 self.mainframes['match_overview'],
                                 row=1, col=1, width=50,
                                 bindings={'<<ListboxSelect>>': self.onselect},
                                 selectmode=tkinter.SINGLE)

    def define_labels_dict(self):
        self.Labels = {}

        """PLayer overview frame"""
        self.add_to_label_dict(self.Labels, 'av_last_match',
                               self.mainframes['player_overview'], row=1,
                               col=1, text='Last match average')
        self.add_to_label_dict(self.Labels, 'av_last_match_val',
                               self.mainframes['player_overview'], row=1,
                               col=2, var=True,
                               text=self.av_last_match)

        self.add_to_label_dict(self.Labels, 'result_last_match',
                               self.mainframes['player_overview'], row=1,
                               col=3, var=True,
                               text=self.result_last_match)

        self.add_to_label_dict(self.Labels, 'highest_fin',
                               self.mainframes['player_overview'], row=2,
                               col=1, text='Highest finish')
        self.add_to_label_dict(self.Labels, 'highest_fin_val',
                               self.mainframes['player_overview'], row=2,
                               col=2, var=True,
                               text=self.highest_fin)

        self.add_to_label_dict(self.Labels, 'highest_av',
                               self.mainframes['player_overview'], row=2,
                               col=3, text='Highest average')
        self.add_to_label_dict(self.Labels, 'highest_av_val',
                               self.mainframes['player_overview'], row=2,
                               col=4, var=True,
                               text=self.highest_av)

        self.add_to_label_dict(self.Labels, 'highest_throw',
                               self.mainframes['player_overview'], row=2,
                               col=5, text='Highest throw')
        self.add_to_label_dict(self.Labels, 'highest_throw_val',
                               self.mainframes['player_overview'], row=2,
                               col=6, var=True,
                               text=self.highest_throw)

        self.add_to_label_dict(self.Labels, 'wins',
                               self.mainframes['player_overview'], row=3,
                               col=1, text='wins')
        self.add_to_label_dict(self.Labels, 'wins_val',
                               self.mainframes['player_overview'], row=4,
                               col=1, var=True,
                               text=self.win_count)

        self.add_to_label_dict(self.Labels, 'losses',
                               self.mainframes['player_overview'], row=3,
                               col=2, text='losses')
        self.add_to_label_dict(self.Labels, 'losses_val',
                               self.mainframes['player_overview'], row=4,
                               col=2, var=True,
                               text=self.loss_count)

        self.add_to_label_dict(self.Labels, 'win_loss_ratio',
                               self.mainframes['player_overview'], row=3,
                               col=3, text='win/loss ratio')
        self.add_to_label_dict(self.Labels, 'win_loss_ratio_val',
                               self.mainframes['player_overview'], row=4,
                               col=3, var=True,
                               text=self.win_loss_ratio)

    def add_to_entry_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1, bindings=None, callback=None,
                          width=10, sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, bindings=bindings,
                         callback=callback, width=width, sticky=sticky)
        return dct

    def add_to_label_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1, width=10, text=None, var=False,
                          sticky=None):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, width=width, text=text,
                         var=var, sticky=sticky)
        return dct

    def add_to_frame_dict(self, dct, name, frame, row, col, rowspan=1,
                          columnspan=1):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan)
        return dct

    def add_to_button_dict(self, dct, name, frame, text, row, col, rowspan=1,
                           columnspan=1, bindings=None, callback=None,
                           width=10, sticky=None, takefocus=1):
        dct[name] = dict(parent=frame, text=text, row=row, column=col,
                         rowspan=rowspan, columnspan=columnspan,
                         bindings=bindings, callback=callback, width=width,
                         sticky=sticky, takefocus=takefocus)
        return dct

    def add_to_listbox_dict(self, dct, name, frame, row, col, rowspan=1,
                            columnspan=1, width=10, bindings=None,
                            selectmode=tkinter.SINGLE):
        dct[name] = dict(parent=frame, row=row, column=col, rowspan=rowspan,
                         columnspan=columnspan, width=width, bindings=bindings,
                         selectmode=selectmode)
        return dct

    def add_to_optionmenu_dict(self, dct, name, frame, row, col, rowspan=1,
                               columnspan=1, width=10, option_list=None):
        dct[name] = dict(parent=frame, name=name, row=row, column=col,
                         rowspan=rowspan, columnspan=columnspan, width=width,
                         option_list=option_list)
        return dct

    def define_labels_match_overview_dict(self):
        match_id = int(self.selected_match_id)

        all_sets = []
        all_legs = []
        row = 1

        self.add_to_label_dict(self.Labels, 'top1',
                               self.mainframes['graph_frame'], row=row,
                               col=1, text='')
        self.add_to_label_dict(self.Labels, 'top2',
                               self.mainframes['graph_frame'], row=row,
                               col=2, var=True,
                               text=self.selected_player)
        self.add_to_label_dict(self.Labels, 'top3',
                               self.mainframes['graph_frame'], row=row,
                               col=3, var=True,
                               text=self.opponent)

        all_set_ids = []

        f_set_id = 1
        for sets in data_load['sets'].values():
            set_id = [int(s_id) for s_id in sets.set_id.split('.')]
            if match_id == set_id[0]:
                all_sets.append(sets)
                all_set_ids.append(set_id[-1])

        all_set_ids_sorted = sorted(all_set_ids)

        for c_set_id in all_set_ids_sorted:
            set_id = '.'.join([str(match_id), str(c_set_id)])
            sets = data_load['sets'][set_id]
            row += 1
            all_leg_ids = list()

            for legs in data_load['legs'].values():
                leg_id = [int(l_id) for l_id in legs.leg_id.split('.')]
                if match_id == leg_id[0] and c_set_id == leg_id[1]:
                    all_legs.append(legs)
                    all_leg_ids.append(leg_id[-1])

            all_leg_ids_sorted = sorted(all_leg_ids)

            for c_leg_id in all_leg_ids_sorted:
                leg_id = '.'.join([str(match_id),
                                   str(c_set_id),
                                   str(c_leg_id)])
                legs = data_load['legs'][leg_id]
                if legs.leg_throws[self.selected_player]:
                    leg_av_pl = np.mean(legs.leg_throws[self.selected_player])
                    leg_average_player = '{:.2f}'.format(leg_av_pl)
                else:
                    leg_average_player = 'No throws'
                if legs.leg_throws[self.opponent]:
                    leg_av_oppo = np.mean(legs.leg_throws[self.opponent])
                    leg_average_oppo = '{:.2f}'.format(leg_av_oppo)
                else:
                    leg_average_oppo = 'No throws'

                col = 1
                input_string = 'Set %s - Leg %s' % (c_set_id, c_leg_id)

                for text in [input_string, leg_average_player,
                             leg_average_oppo]:
                    name = col + (row - 1) * 3
                    self.add_to_label_dict(
                        dct=self.Labels, name=name,
                        frame=self.mainframes['graph_frame'],
                        col=col, row=row, text=text)
                    col += 1
                row += 1

            f_set_id += 1
            col = 1
            for text in ['', '', '']:
                name = col + (row - 1) * 3
                self.add_to_label_dict(dct=self.Labels, name=name,
                                       frame=self.mainframes['graph_frame'],
                                       col=col, row=row, text=text)
                col += 1

    def define_optionmenus_dict(self):
        self.Optionmenus = {}

        self.add_to_optionmenu_dict(self.Optionmenus, name='playermenu',
                                    frame=self.mainframes['top_frame'],
                                    row=1, col=1, option_list=self.players)

    def create_entry(self, parent, row, column, rowspan, columnspan, width,
                     bindings, callback, sticky):
        new_entry = tkinter.Entry(parent, width=width)
        if callback is None:
            for binding, callback in bindings.items():
                new_entry.bind(binding, callback)
        else:
            new_entry.config(command=callback)
        new_entry.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, sticky=sticky)
        return new_entry

    def create_button(self, parent, text, row, column, rowspan, columnspan,
                      bindings, callback, width, sticky, takefocus):
        new_button = ttk.Button(parent, text=text, takefocus=takefocus)
        if callback is None:
            for binding, callback in bindings.items():
                new_button.bind(binding, callback)
        else:
            new_button.config(command=callback)

        new_button.grid(row=row, column=column, rowspan=rowspan,
                        columnspan=columnspan, sticky=sticky)
        return new_button

    def create_frame(self, parent, row, column, rowspan, columnspan):
        new_frame = tkinter.Frame(parent)
        new_frame.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan)
        return new_frame

    def create_listbox(self, parent, row, column, rowspan, columnspan, width,
                       bindings, selectmode):
        new_listbox = tkinter.Listbox(parent, width=width,
                                      selectmode=selectmode)
        new_listbox.grid(row=row, column=column, rowspan=rowspan,
                         columnspan=columnspan)
        if bindings is not None:
            for binding, callback in bindings.items():
                new_listbox.bind(binding, callback)
        return new_listbox

    def create_labels(self, dct, name, parent, row, column, rowspan,
                      columnspan, width, var, text, sticky):
        if var:
            dct[name]['textvar'] = tkinter.StringVar()
            dct[name]['textvar'].set(text)
            new_label = tkinter.Label(parent,
                                      textvariable=dct[name]['textvar'])

        else:
            new_label = tkinter.Label(parent, text=text)

        new_label.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, sticky=sticky)

        return new_label

    def create_optionmenu(self, name, parent, row, column, rowspan, columnspan,
                          width, option_list):
        variable = tkinter.StringVar()
        new_optionmenu = tkinter.OptionMenu(parent, variable, *option_list)

        new_optionmenu.grid(row=row, column=column, rowspan=rowspan,
                            columnspan=columnspan)
        new_optionmenu.config(width=width)

        variable.set(option_list[0])
        variable.trace("w", lambda *args: self.option_changed(variable))
        return new_optionmenu, variable

    def filling_listbox(self, listbox):
        listbox.delete(0, tkinter.END)
        for item in self.list_of_strings:
            listbox.insert(0, item)

    def option_changed(self, varia):
        """When player is selected, change the labels"""
        self.selected_player = varia.get()
        self.getting_playerstats(varia.get(), data_load)
        self.filling_listbox(self.listboxes['match_box'])
        self.listboxes['match_box'].selection_clear(0, tkinter.END)
        self.listboxes['match_box'].selection_set(0)
        self.remove_labels()
        self.define_labels_dict()
        for name, label in self.Labels.items():
            self.labels[name]['label'] = self.create_labels(self.labels,
                                                            name=name, **label)
        self.print_match_stats(self.listboxes['match_box'])

    def onselect(self, event):
        """Change labels in graphframe, when match is selected"""
        w = event.widget
        self.print_match_stats(w)

    def remove_labels(self):
        for name, label in self.Labels.items():
            if label['parent'] == self.mainframes['graph_frame']:
                self.labels[name]['label'].grid_forget()
                self.labels[name]['label'].destroy()
                del self.labels[name], self.Labels[name]

    def print_match_stats(self, widget):
        index = int(widget.curselection()[0])
        value = widget.get(index)

        self.remove_labels()

        self.selected_match_id = value.split()[0]

        self.selected_match = data_load['matches'][int(self.selected_match_id)]
        self.opponent = [player for player in self.selected_match.players
                         if player != self.selected_player][0]

        self.define_labels_match_overview_dict()

        for name, label in self.Labels.items():
            if label['parent'] == self.mainframes['graph_frame']:
                self.labels[name]['label'] = self.create_labels(
                                                        self.Labels,
                                                        name=name,
                                                        **label)

    def savefigure(self, event):
        fig, ax = plt.subplots(1, 1)
        bins = range(np.min(self.all_throws), np.max(self.all_throws) + 1, 1)
        plt.hist(self.all_throws, bins=bins, color="#87CEFA", edgecolor='none')
        pl_mean = np.mean(self.all_throws)
        all_throws_no_zeros = [val for val in self.all_throws if val != 0]
        pl_mode = np.argmax(np.bincount(all_throws_no_zeros))
        pl_highest = np.max(self.all_throws)
        pl_lowest = np.min(all_throws_no_zeros)
        plt.axvline(pl_mean, color='r')

        text = "Average:\nMost frequent throw:\nHighest throw:\nLowest throw:"
        values = "{:>.2f}\n{:>d}\n{:>d}\n{:>d}".format(pl_mean, pl_mode,
                                                       pl_highest, pl_lowest)
        ax.text(0.5, 0.8, text, transform=ax.transAxes, ha='left', fontsize=14)
        ax.text(0.9, 0.8, values, transform=ax.transAxes, ha='right',
                fontsize=14)

        fig.savefig("../../histogram_%s.png" % self.selected_player)

    # filling player overview
    def getting_playerstats(self, name, data):
        all_matches = []
        all_match_ids = []
        self.all_throws = []
        all_averages = []
        all_dates = []
        all_finishes = []

        all_sets = []
        all_legs = []

        self.win_count = 0
        self.loss_count = 0

        self.list_of_strings = []

        for match in data['matches'].values():
            if name in match.players:
                name_opp = [item for item in match.players if item != name][0]
                all_matches.append(match)
                all_match_ids.append(match.match_id)
                self.all_throws += match.match_throws[name]
                if match.match_throws[name]:
                    all_averages.append(np.mean(match.match_throws[name]))
                all_dates.append(match.date_tag)
                if match.won_by is not None and match.lost_by is not None:
                    if match.won_by == name:
                        self.win_count += 1
                    elif match.lost_by == name:
                        self.loss_count += 1

                format_string = '{:<4d}{:<20s}{:<10s}{:<10s}{:>3d}{:>3d}'
                string = format_string.format(
                    match.match_id,
                    datetime.strftime(match.date_tag,
                                      "%Y-%m-%d %H:%M"),
                    name, name_opp, match.bo_sets,
                    match.bo_legs)
                self.list_of_strings.append(string)

        for match in all_matches:
            for sets in data['sets'].values():
                if sets.set_id.split('.')[0] == str(match.match_id):
                    all_sets.append(sets)
            for leg in data['legs'].values():
                if leg.leg_id.split('.')[0] == str(match.match_id):
                    all_legs.append(leg)
                    if leg.won_by == self.selected_player:
                        all_finishes.append(leg.finish)

        if all_finishes:
            self.highest_fin = np.max(all_finishes)
        else:
            self.highest_fin = 'Never finished'

        self.highest_av = '{:.2f}'.format(np.max(all_averages))
        self.highest_throw = np.max(self.all_throws)
        self.av_last_match = '{:.2f}'.format(all_averages[-1])
        last_match_id = all_match_ids.index(np.max(all_match_ids))
        if name == all_matches[last_match_id].won_by:
            self.result_last_match = 'win'
        elif name == all_matches[last_match_id].lost_by:
            self.result_last_match = 'lose'
        else:
            self.result_last_match = 'Did not finish last match'

        if self.loss_count == 0 and self.win_count != 0:
            self.win_loss_ratio = 'Only wins bitch!'
        elif self.loss_count == 0 and self.win_count == 0:
            self.win_loss_ratio = 'No games finished yet'
        else:
            ratio = float(self.win_count)/float(self.loss_count)
            self.win_loss_ratio = '{:.2f}'.format(ratio)

if __name__ == "__main__":
    import logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    format_logger = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(format_logger)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    fname = 'database.pkl'

    if os.path.isfile(fname):
        with open(fname, 'rb') as fp:
            if sys.version[0] == str(2):
                data_load = pickle.load(fp)
            else:
                data_load = pickle.load(fp, encoding='bytes')
    else:
        logger.info("file not available")

    overview = overview()
