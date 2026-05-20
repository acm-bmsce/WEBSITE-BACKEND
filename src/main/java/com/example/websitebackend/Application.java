package com.example.websitebackend;

import com.example.websitebackend.config.AppProperties; // ✅ Add this import
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties; // ✅ Add this import

@SpringBootApplication
@EnableConfigurationProperties(AppProperties.class) // ✅ Add this annotation
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}