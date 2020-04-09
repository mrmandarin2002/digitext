package sample;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class OptionBox {
    private static boolean answer;

    public static boolean display(String title, String question){
        Stage window = new Stage();

        window.initModality(Modality.APPLICATION_MODAL);
        window.setTitle(title);
        window.setMinWidth(250);
        window.getIcons().add(new Image("/icons/error_icon.png"));

        Label label = new Label();
        label.setText(question);
        Button yes_button = new Button("Oui");
        yes_button.setFocusTraversable(false);
        yes_button.setOnAction(e->{
            answer = true;
            window.close();
        });
        Button no_button = new Button("Nein");
        no_button.setFocusTraversable(false);
        no_button.setOnAction(e->{
           answer = false;
           window.close();
        });
        VBox layout = new VBox(10);
        HBox bottom_layout = new HBox(10);
        bottom_layout.getChildren().addAll(yes_button, no_button);
        layout.getChildren().addAll(label);
        layout.setAlignment(Pos.CENTER);
        layout.setPadding(new Insets(12,12,12,12));
        BorderPane box_layout = new BorderPane();
        box_layout.setCenter(layout);
        box_layout.setBottom(bottom_layout);
        Scene scene = new Scene(box_layout);
        window.setScene(scene);
        window.showAndWait();
        return answer;
    }
}
