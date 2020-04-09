package sample;

        import javafx.beans.property.BooleanProperty;
        import javafx.beans.property.SimpleBooleanProperty;
        import javafx.scene.image.Image;
        import javafx.scene.image.ImageView;

public class Status_boolean {
    private Image red_dot = new Image("/icons/red_dot_icon.png");
    private ImageView red_dot_icon = new ImageView(red_dot);

    private Image green_dot = new Image("/icons/green_dot_icon.png");
    private ImageView green_dot_icon = new ImageView(green_dot);

    private BooleanProperty Bool = new SimpleBooleanProperty(this, "Bool", false);

    public BooleanProperty BoolProperty(){
        return Bool;
    }

    public boolean getBool(){
        return Bool.get();
    }

    public void setBool(boolean BoolName){
        //System.out.println(this.getClass().getSimpleName() + " is set to " + BoolName);
        this.Bool.set(BoolName);
    }

    public ImageView getImageView(){
        red_dot_icon.setFitHeight(11);
        red_dot_icon.setFitWidth(11);
        green_dot_icon.setFitHeight(11);
        green_dot_icon.setFitWidth(11);
        if(Bool.get()){
            return green_dot_icon;
        } else{
            return red_dot_icon;
        }
    }

    public Image getImage(){
        if(Bool.get()){
            return green_dot;
        } else{
            return red_dot;
        }
    }

    public void flipBool(){
        this.Bool.set(!Bool.get());
        System.out.println(this.getClass().getSimpleName() + " is now set to " + Bool.get());
    }
}
