<?php
/*
Plugin Name: Contact Form Microfrontend
Description: Embeds a custom web component contact form (<x-contact-form />) into posts or pages.
Version: 1.0
Author: Your Name
*/

function cf_microfrontend_enqueue_script() {
    wp_register_script(
        'contact-form-microfrontend',
        plugins_url('js/contact-form.js', __FILE__),
        [],
        null,
        true
    );
    wp_enqueue_script('contact-form-microfrontend');
}
add_action('wp_enqueue_scripts', 'cf_microfrontend_enqueue_script');

// [contact_form_microfrontend] shortcode
function cf_microfrontend_shortcode() {
    return '<x-subscriberform></x-subscriberform>';
}
add_shortcode('contact_form_microfrontend', 'cf_microfrontend_shortcode');
