# Proyecto 2 de la Unidad 2 / Programación 1 / Matías Fonseca, Claudio Larosa.
import pandas 
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio
from gi.repository import GdkPixbuf

class Drogas_principal:

    def __init__(self):

        builder = Gtk.Builder()
        builder.add_from_file("proyecto2.ui")

        # Configuración ventana principal.
        self.window = builder.get_object("main")
        # self.window.set_title("Reseña Medicamentos")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.maximize()

        # Se crea un Headerbar como en el ejemplo que mando.
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Medicamentos PVC"
        self.window.set_titlebar(hb)

        # Se crea una box para contener botones (sacado del ejemplo)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        # Botón Filechooser con su ícono y su imagen de Documento Abierto (sacado del ejemplo).
        boton = Gtk.Button() 
        icono = Gio.ThemedIcon(name="document-open")
        imagen = Gtk.Image.new_from_gicon(icono, Gtk.IconSize.BUTTON)
        boton.add(imagen)
        boton.connect("clicked", self.dialogo_filechooser)
        box.add(boton)
        hb.pack_start(box)

        # Botón About con su ícono y su imagen de Ayuda (sacado del ejemplo).
        boton1 = Gtk.Button()
        icon = Gio.ThemedIcon(name="help-about")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        boton1.add(image)
        hb.pack_end(boton1)
        boton1.connect("clicked", self.dialogo_ayuda)

        # Se configura un TreeView para la vista de los datos (sacado del ejemplo).
        self.tree = builder.get_object("medicamentos")
        self.tree.connect("row-activated", self.activar_tree_row)
        self.tree.set_activate_on_single_click(True)

        # Se configura el Gtk.Paned (sacado del ejemplo).
        paned = builder.get_object("paned_window")
        paned.connect("size-allocate", self.paned_resize)

        # Se agrega función al label del Gtk.Paned (sacado del ejemplo).
        self.informacion = builder.get_object("informacion")
        self.informacion.set_halign(Gtk.Align.START)
        self.informacion.set_valign(Gtk.Align.START)
        self.informacion.set_margin_start(50)
        self.informacion.set_margin_top(50)       

        # Botón para editar los medicamentos.
        boton2 = builder.get_object("edit")
        boton2.set_label("Editar Medicamento")
        #boton2.connect("clicked", self.abrir_edicion)

        # Botón que abre resument (incompleto)
        boton3 = builder.get_object("resume")
        boton3.set_label("Resumen")
        #boton3.connect("clicked", self.abrir_resumen)

        self.window.show_all()

    # Función de configuración de tamaño para el Gtk.Paned.
    def paned_resize(self, widget, allocation):
        
        hpaned_pos = 1
        if allocation.width != 1:
            hpaned_pos = 0.3 * allocation.width
        widget.set_position(int(hpaned_pos + .5))

    # Función para el Botón de Selección de Archivos.
    def dialogo_filechooser(self, btn=None):
        """Diálogo de selección de archivos"""

        filechooser = Gtk.FileChooserDialog()
        filechooser.set_title("Selecciona un archivo")
        filechooser.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        filechooser.set_action(Gtk.FileChooserAction.OPEN)

        filter_csv = Gtk.FileFilter()
        filter_csv.add_mime_type("text/csv")
        filter_csv.set_name("Archivos CSV")
        filechooser.add_filter(filter_csv)

        response = filechooser.run()

        if response == Gtk.ResponseType.OK:
            filepath = filechooser.get_filename()
            self.ver_archivos(filepath)
        
        filechooser.destroy()

    # Función para el Botón Acerca de.
    def dialogo_ayuda(self, btn=None):
        """Diálogo Acerca de."""
        # print("Click")
        about = Gtk.AboutDialog()
        about.set_modal(True)
        about.set_title("Acerca De")
        about.set_program_name("Interfaz Medicamentos PVC")
        about.set_name("Proyecto 2")
        about.set_authors(["Matías Fonseca", "Claudio Larosa"])
        about.set_comments("Esta es la interfaz de uso de Medicamentos PVC")
        about.set_logo_icon_name("go-home")

        about.run()
        about.destroy()

    # Función para ver archivos en la ventana principal.
    def ver_archivos(self, pathfile):
        
        # Se lee el archivo csv.
        data_pd = pandas.read_csv(pathfile)

        if self.tree.get_columns():
            for column in self.tree.get_columns():
                self.tree.remove_column(column)

        largo_columnas = len(data_pd.columns)
        modelo = Gtk.ListStore(*(largo_columnas * [str]))
        self.tree.set_model(model=modelo)

        cell = Gtk.CellRendererText()

        for item in range(len(data_pd.columns)):
            column = Gtk.TreeViewColumn(data_pd.columns[item],
                                        cell,
                                        text=item)
            self.tree.append_column(column)
            column.set_sort_column_id(item)
            # Las columnas review y fecha se esconden.
            if item > 1:
                column.set_visible(False)

        for item in data_pd.values:
            line = [str(x) for x in item]
            modelo.append(line)

    def activar_tree_row(self, model, path, iter_):
        """Cambios en el TreeView"""

        model, it = self.tree.get_selection().get_selected()
        if model is None:
            return False
        
        text = "<b>Datos no mostrados: </b> \n\n"
        for i in range(2, 6):
            text = f"{text}<b>{self.tree.get_column(i).get_title()}: </b> \n"
            text = f"{text} {model.get_value(it, i)} \n"
            text = f"\n {text} \n"
        # Aplica texto concatenado al label con lo que dice en las columnas ocultas.
        self.informacion.set_markup(text)

if __name__ == "__main__":
    Drogas_principal()
    Gtk.main()