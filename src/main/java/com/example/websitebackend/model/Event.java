package com.example.websitebackend.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field; // ✅ Import this!
import lombok.Data; // Assuming you are using Lombok for getters/setters

import java.util.Date;
import java.util.List;

@Data
@Document(collection = "events")
public class Event {

    @Id
    private String id;

    private String title;

    private String description;

    // ✅ Use java.util.Date to perfectly match the MongoDB "$date" object
    private Date date;

    private String image;

    private String fullDescription;

    private String outcomes;

    private List<String> gallery;

    private String location;

    private Integer attendees;

    // ✅ Tells Java to look for the Python snake_case name in the database
    @Field("registration_link")
    private String registrationLink;

    // ✅ Tells Java to look for the Python snake_case name in the database
    @Field("is_featured")
    private Boolean featured;
}