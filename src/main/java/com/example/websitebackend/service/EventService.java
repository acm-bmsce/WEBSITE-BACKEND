package com.example.websitebackend.service;

import com.example.websitebackend.dto.EventCreateRequest;
import com.example.websitebackend.dto.EventUpdateRequest;
import com.example.websitebackend.model.Event;
import com.example.websitebackend.repository.EventRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

@Service
@RequiredArgsConstructor
public class EventService {

    private final EventRepository eventRepository;
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("dd-MM-yyyy");

    public Page<Event> getEvents(int skip, int limit, Boolean featured) {
        // Spring uses PageRequest(page_number, size) instead of skip/limit
        int page = skip / limit;
        Pageable pageable = PageRequest.of(page, limit, Sort.by(Sort.Direction.DESC, "date"));

        if (featured != null) {
            return eventRepository.findByIsFeatured(featured, pageable);
        }
        return eventRepository.findAll(pageable);
    }

    public Event createEvent(EventCreateRequest request) {
        Event event = new Event();
        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());

        try {
            event.setDate(LocalDate.parse(request.getDateStr(), DATE_FORMATTER).atStartOfDay());
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Invalid date format. Use DD-MM-YYYY");
        }

        event.setImage(request.getImage());
        event.setFullDescription(request.getFullDescription());
        event.setOutcomes(request.getOutcomes());
        if (request.getGallery() != null) event.setGallery(request.getGallery());
        event.setLocation(request.getLocation());

        try {
            if (request.getAttendees() != null) {
                event.setAttendees(Integer.parseInt(request.getAttendees()));
            }
        } catch (NumberFormatException ignored) {}

        event.setRegistrationLink(request.getRegistrationLink());
        event.setFeatured(request.isFeatured());

        return eventRepository.save(event);
    }

    public Event updateEvent(String eventId, EventUpdateRequest request) {
        Event event = eventRepository.findById(eventId)
                .orElseThrow(() -> new IllegalArgumentException("Event not found"));

        if (request.getTitle() != null) event.setTitle(request.getTitle());
        if (request.getDescription() != null) event.setDescription(request.getDescription());

        if (request.getDateStr() != null) {
            try {
                event.setDate(LocalDate.parse(request.getDateStr(), DATE_FORMATTER).atStartOfDay());
            } catch (DateTimeParseException e) {
                throw new IllegalArgumentException("Invalid date format. Use DD-MM-YYYY");
            }
        }

        if (request.getImage() != null) event.setImage(request.getImage());
        if (request.getFullDescription() != null) event.setFullDescription(request.getFullDescription());
        if (request.getOutcomes() != null) event.setOutcomes(request.getOutcomes());
        if (request.getGallery() != null) event.setGallery(request.getGallery());
        if (request.getLocation() != null) event.setLocation(request.getLocation());
        if (request.getAttendees() != null) event.setAttendees(request.getAttendees());
        if (request.getRegistrationLink() != null) event.setRegistrationLink(request.getRegistrationLink());
        if (request.getIsFeatured() != null) event.setFeatured(request.getIsFeatured());

        return eventRepository.save(event);
    }

    public void deleteEvent(String eventId) {
        if (!eventRepository.existsById(eventId)) {
            throw new IllegalArgumentException("Event not found");
        }
        eventRepository.deleteById(eventId);
    }
}