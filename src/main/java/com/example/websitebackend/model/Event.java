package com.example.websitebackend.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.index.CompoundIndexes;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Data
@Document(collection = "events")
@CompoundIndexes({
        @CompoundIndex(name = "featured_date_idx", def = "{'is_featured': 1, 'date': -1}")
})
public class Event {

    @Id
    private String id;

    private String title;
    private String description;

    @Indexed
    private LocalDateTime date;

    private String image;

    @Field("fullDescription") // Ensure it matches Mongo field
    private String fullDescription;

    private String outcomes;
    private List<String> gallery = new ArrayList<>();
    private String location;
    private int attendees = 0;

    @Field("registration_link")
    private String registrationLink;

    @Field("is_featured")
    @Indexed
    private boolean isFeatured = false;
}