package com.example.websitebackend.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Data // Lombok automatically creates getters, setters, and constructors
@Document(collection = "users") // Equivalent to Beanie's Settings.name = "users"
public class User {

    @Id
    private String id; // MongoDB requires an explicit ID field in Java

    @Indexed(unique = true)
    private String username;

    @Indexed(unique = true)
    private String email;

    @Field("hashed_password") // Ensures it matches your DB column exactly
    private String hashedPassword;

    private String role = "coordinator"; // Default value

    @Field("is_approved")
    private boolean isApproved = false;

    @Field("reset_requested") // Tracks if they forgot their password
    private boolean resetRequested = false;
}