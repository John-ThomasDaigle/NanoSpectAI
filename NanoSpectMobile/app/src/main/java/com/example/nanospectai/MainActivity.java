package com.example.nanospectai;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import android.net.Uri;
import android.os.Environment;

import androidx.appcompat.app.AppCompatCallback;
import androidx.appcompat.widget.AppCompatButton;
import androidx.core.content.FileProvider;
import java.io.File;
import java.io.IOException;
import java.io.FileOutputStream;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import android.media.ExifInterface;
import android.graphics.Matrix;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CODE = 22; // Code to identify camera result
    Button btnpicture;
    ImageView imageView;
    File currentPhotoFile; // The file where the current photo is saved
    Uri imageUri; // URI pointing to the current photo file
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT); // Locks screen to portrait

        // Bind UI elements
        btnpicture= findViewById(R.id.btncamera_id);
        imageView= findViewById(R.id.imageview1);
        AppCompatButton btnDelete = findViewById(R.id.btndelete_id);
        AppCompatButton btnStop = findViewById(R.id.btnstop_id);

        // Open camera when camera button is tapped
        btnpicture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

                // Create a file to save the photo into
                File photoFile = null;
                try{
                    photoFile = createImageFile();
                    currentPhotoFile = photoFile;
                } catch(IOException e){
                    e.printStackTrace();
                }

                if (photoFile != null){
                    // Get a shareable URI for the file via FileProvider
                    imageUri = FileProvider.getUriForFile(
                            MainActivity.this,
                            getPackageName() + ".provider",
                            photoFile
                    );

                    // Tell the camera where to save the photo
                    cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
                    cameraIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                    cameraIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

                    startActivityForResult(cameraIntent, REQUEST_CODE);
                }
            }
        });

        // Show confirmation dialog before deleting all saved images
        btnDelete.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                File storageDir = new File(getExternalFilesDir(null), "NanoSpectAI_Images");
                File[] files = storageDir.listFiles();

                if (files == null || files.length == 0) {
                    Toast.makeText(MainActivity.this, "No images found", Toast.LENGTH_SHORT).show();
                    return;
                }

                new androidx.appcompat.app.AlertDialog.Builder(MainActivity.this)
                        .setTitle("Delete Images")
                        .setMessage("Are you sure you want to delete all images?")
                        .setPositiveButton("Yes", (dialog, which) -> {
                            deleteAllImages();
                        })
                        .setNegativeButton("Cancel", (dialog, which) -> {
                            dialog.dismiss();
                        })
                        .show();
            }
        });

        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new androidx.appcompat.app.AlertDialog.Builder(MainActivity.this)
                        .setTitle("Send STOP")
                        .setMessage("Are you sure you want to send STOP?")
                        .setPositiveButton("Yes", (dialog, which) -> {
                            sendStopFile();
                        })
                        .setNegativeButton("Cancel", (dialog, which) -> {
                            dialog.dismiss();
                        })
                        .show();
            }
        });
    }
    // Name images sequentially (image_1, image_2, ...)
    private File createImageFile() throws IOException {

        File storageDir = new File(getExternalFilesDir(null), "NanoSpectAI_Images");

        if (!storageDir.exists()) {
            storageDir.mkdirs();
        }

        // Find the next available image number
        int imageNumber = 1;
        File imageFile;
        do {
            String fileName = "image_" + imageNumber + ".jpeg";
            imageFile = new File(storageDir, fileName);
            imageNumber++;
        } while (imageFile.exists());

        return imageFile;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        if(requestCode == REQUEST_CODE && resultCode == RESULT_OK)
        {
            if (currentPhotoFile != null) {
                Toast.makeText(this, "Saved: " + currentPhotoFile.getAbsolutePath(), Toast.LENGTH_LONG).show();
            }
            try {
                // Load the captured bitmap from URI
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(
                        this.getContentResolver(),
                        imageUri
                );

                // Fix rotation
                bitmap = fixRotation(bitmap, currentPhotoFile);

                // Resize to 25%
                int width = bitmap.getWidth() / 4;
                int height = bitmap.getHeight() / 4;
                Bitmap resizedBitmap = Bitmap.createScaledBitmap(bitmap, width, height, true);

                // Show in ImageView
                imageView.setImageBitmap(resizedBitmap);

                // Save to file
                FileOutputStream out = new FileOutputStream(currentPhotoFile);
                resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 100, out);
                out.flush();
                out.close();

                // Send via Bluetooth
                sendImageBluetooth(imageUri);

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        else{
            Toast.makeText(this, "Cancelled", Toast.LENGTH_SHORT).show();
        }

        super.onActivityResult(requestCode, resultCode, data);
    }

    private Bitmap fixRotation(Bitmap bitmap, File file) {
        try {
            // Read EXIF orientation from file
            ExifInterface exif = new ExifInterface(file.getAbsolutePath());
            int orientation = exif.getAttributeInt(
                    ExifInterface.TAG_ORIENTATION,
                    ExifInterface.ORIENTATION_NORMAL
            );

            Matrix matrix = new Matrix();

            // Set rotation angle based on orientation
            if (orientation == ExifInterface.ORIENTATION_ROTATE_90)
                matrix.postRotate(90);
            else if (orientation == ExifInterface.ORIENTATION_ROTATE_180)
                matrix.postRotate(180);
            else if (orientation == ExifInterface.ORIENTATION_ROTATE_270)
                matrix.postRotate(270);

            // Return rotated bitmap
            return Bitmap.createBitmap(
                    bitmap,
                    0,
                    0,
                    bitmap.getWidth(),
                    bitmap.getHeight(),
                    matrix,
                    true
            );

        } catch (Exception e) {
            e.printStackTrace();
        }

        return bitmap;
    }

    // Deletes every file in the NanoSpectAI_Images folder
    private void deleteAllImages() {

        File storageDir = new File(getExternalFilesDir(null), "NanoSpectAI_Images");
        File[] files = storageDir.listFiles();

        if (files != null) {
            for (File file : files) {
                file.delete();
            }
        }

        Toast.makeText(this, "Images have been deleted", Toast.LENGTH_SHORT).show();
    }

    // Opens the share menu
    private void sendImageBluetooth(Uri uri) {

        Intent intent = new Intent(Intent.ACTION_SEND);
        intent.setType("image/jpeg");
        intent.putExtra(Intent.EXTRA_STREAM, uri);
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

        startActivity(Intent.createChooser(intent, "Send Image"));
    }

    private void sendStopFile() {
        try {
            File storageDir = new File(getExternalFilesDir(null), "NanoSpectAI_Images");

            if (!storageDir.exists()) {
                storageDir.mkdirs();
            }

            File stopFile = new File(storageDir, "STOP.txt");

            FileOutputStream fos = new FileOutputStream(stopFile);
            fos.write("STOP".getBytes());
            fos.flush();
            fos.close();

            Uri uri = FileProvider.getUriForFile(
                    this,
                    getPackageName() + ".provider",
                    stopFile
            );

            Intent intent = new Intent(Intent.ACTION_SEND);
            intent.setType("text/plain");
            intent.putExtra(Intent.EXTRA_STREAM, uri);
            intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);

            startActivity(Intent.createChooser(intent, "Send STOP"));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}