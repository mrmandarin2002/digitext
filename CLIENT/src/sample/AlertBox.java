package sample;

import javafx.fxml.FXMLLoader;
import javafx.scene.image.Image;
import javafx.stage.*;
import javafx.scene.*;
import javafx.scene.layout.*;
import javafx.scene.control.*;
import javafx.geometry.*;

public class AlertBox {
    public static void display(String title, String message, String button_message){

        Stage window = new Stage();

        window.initModality(Modality.APPLICATION_MODAL);
        window.setTitle(title);
        window.setMinWidth(250);
        window.getIcons().add(new Image("/icons/error_icon.png"));

        Label label = new Label();
        label.setText(message);
        Button closeButton = new Button(button_message);
        closeButton.setFocusTraversable(false);
        closeButton.setOnAction(e -> window.close());

        VBox layout = new VBox(10);
        layout.getChildren().addAll(label, closeButton);
        layout.setAlignment(Pos.CENTER);
        layout.setPadding(new Insets (12,12,12,12));

        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();
    }

}
